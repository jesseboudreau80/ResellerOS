from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, services
from ..database import get_db

router = APIRouter(prefix="/barcode", tags=["barcode"])


@router.post("/item/{sku}")
def generate_item_barcode(sku: str, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == sku).first()
    if not item:
        return {"error": "Item not found"}
    value = item.barcode if item.barcode_type in {"UPC", "EAN"} else item.sku
    return {"barcode_path": services.generate_barcode_image(value, sku)}
