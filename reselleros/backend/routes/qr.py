from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, services
from ..database import get_db

router = APIRouter(prefix="/qr", tags=["qr"])


@router.post("/item/{sku}")
def generate_item_qr(sku: str, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.sku == sku).first()
    if not item:
        return {"error": "Item not found"}
    return {"qr_path": services.generate_qr_image(sku)}
