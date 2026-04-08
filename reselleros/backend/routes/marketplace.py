from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, services
from ..connectors import ebay_connector, facebook_connector, mercari_connector
from ..database import get_db

router = APIRouter(prefix="/marketplace", tags=["marketplace"])


def enqueue(db: Session, item_id: int, action: str):
    job = models.Job(item_id=item_id, action=action, status="queued")
    db.add(job)
    db.commit()
    return job


@router.post("/publish/ebay")
def publish_ebay(payload: schemas.MarketplaceRequest, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == payload.sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    job = enqueue(db, item.id, "publish_ebay")
    return {"job_id": job.id, "status": job.status}


@router.post("/publish/facebook")
def publish_facebook(payload: schemas.MarketplaceRequest, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == payload.sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    job = enqueue(db, item.id, "publish_facebook")
    return {"job_id": job.id, "status": job.status}


@router.post("/publish/mercari")
def publish_mercari(payload: schemas.MarketplaceRequest, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == payload.sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    job = enqueue(db, item.id, "publish_mercari")
    return {"job_id": job.id, "status": job.status}


@router.post("/listing_generator")
def run_listing_generator(payload: schemas.ListingGeneratorInput):
    return services.listing_generator(
        payload.title,
        payload.category,
        payload.condition,
        payload.photos,
        payload.price,
    )


def process_job(db: Session, job: models.Job):
    item = db.query(models.Item).filter(models.Item.id == job.item_id).first()
    if not item:
        raise RuntimeError("Item not found")

    if job.action == "publish_ebay":
        result = ebay_connector.create_listing(item)
        item.ebay_listing_id = result["listing_id"]
        item.ebay_url = result["url"]
    elif job.action == "publish_facebook":
        result = facebook_connector.create_listing(item)
        item.facebook_url = result["url"]
    elif job.action == "publish_mercari":
        result = mercari_connector.create_listing(item)
        item.mercari_url = result["url"]
    elif job.action == "end_listing":
        ebay_connector.end_listing(item)
        facebook_connector.end_listing(item)
        mercari_connector.end_listing(item)
    else:
        raise RuntimeError(f"Unknown action {job.action}")

    item.status = "listed" if job.action.startswith("publish") else "available"
    job.status = "completed"
    job.processed_at = datetime.utcnow()
    services.log_activity(db, item.id, "listing_published", f"Action {job.action}")
