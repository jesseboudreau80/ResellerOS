from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, services
from ..database import get_db

router = APIRouter(prefix="/warehouse", tags=["warehouse"])


@router.post("/locations")
def create_location(location_code: str, description: str = "", db: Session = Depends(get_db)):
    location = models.WarehouseLocation(location_code=location_code, description=description)
    db.add(location)
    db.commit()
    return {"status": "created", "location_code": location_code}


@router.get("/locations")
def list_locations(db: Session = Depends(get_db)):
    return db.query(models.WarehouseLocation).order_by(models.WarehouseLocation.location_code).all()


@router.post("/move/{sku}")
def move_item(sku: str, payload: schemas.MoveItemRequest, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    location = (
        db.query(models.WarehouseLocation)
        .filter(models.WarehouseLocation.location_code == payload.location_code)
        .first()
    )
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    item.shelf_location = payload.location_code
    db.commit()
    services.log_activity(db, item.id, "item_moved", f"Moved to {payload.location_code}")
    return {"status": "moved", "sku": sku, "location": payload.location_code}
