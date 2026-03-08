from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, services
from ..database import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/create", response_model=schemas.ItemOut)
def create_item(payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    sku = services.generate_sku(db)
    barcode_value = payload.barcode or sku
    barcode_type = payload.barcode_type or "CODE128"
    item = models.Item(
        sku=sku,
        barcode=barcode_value,
        barcode_type=barcode_type,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        condition=payload.condition,
        price=payload.price,
        cost=payload.cost,
        shelf_location=payload.shelf_location,
        status="available",
        profit=payload.price - payload.cost,
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    services.generate_barcode_image(barcode_value, sku)
    services.generate_qr_image(sku)
    services.log_activity(db, item.id, "item_created", f"Created item {sku}")
    return item


@router.post("/quick_add", response_model=schemas.ItemOut)
def quick_add(db: Session = Depends(get_db)):
    return create_item(schemas.ItemCreate(), db)


@router.post("/bulk_quick_add")
def bulk_quick_add(payload: schemas.QuickAddBatch, db: Session = Depends(get_db)):
    created = [quick_add(db) for _ in range(payload.count)]
    return {"count": len(created), "items": created}


@router.get("", response_model=list[schemas.ItemOut])
def list_items(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Item)
    if status:
        query = query.filter(models.Item.status == status)
    return query.order_by(models.Item.date_added.desc()).all()


@router.get("/{sku}", response_model=schemas.ItemOut)
def get_item(sku: str, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{sku}", response_model=schemas.ItemOut)
def update_item(sku: str, payload: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    item.profit = (item.price or 0) - (item.cost or 0)
    db.commit()
    db.refresh(item)
    services.log_activity(db, item.id, "item_updated", f"Updated item {sku}")
    return item


@router.delete("/{sku}")
def delete_item(sku: str, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    services.log_activity(db, None, "item_deleted", f"Deleted item {sku}")
    return {"status": "deleted"}


@router.post("/{sku}/mark_sold")
def mark_sold(sku: str, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.status = "sold"
    item.date_sold = datetime.utcnow()
    db.commit()
    services.log_activity(db, item.id, "item_sold", f"Item {sku} sold")
    return {"status": "sold", "sku": sku}


@router.post("/{sku}/generate_qr")
def generate_qr(sku: str, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"qr_path": services.generate_qr_image(sku)}


@router.post("/{sku}/generate_barcode")
def generate_barcode(sku: str, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    value = item.barcode if item.barcode_type in {"UPC", "EAN"} else item.sku
    return {"barcode_path": services.generate_barcode_image(value, sku)}
