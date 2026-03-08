from pathlib import Path

import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads" / "items"


def generate_sku(db: Session) -> str:
    max_id = db.query(func.max(models.Item.id)).scalar() or 0
    return f"RS-{max_id + 1:06d}"


def ensure_item_dir(sku: str) -> Path:
    path = UPLOAD_DIR / sku
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_barcode_image(value: str, sku: str) -> str:
    item_dir = ensure_item_dir(sku)
    barcode_path = item_dir / "barcode"
    code = Code128(value, writer=ImageWriter())
    filename = code.save(str(barcode_path))
    return filename


def generate_qr_image(sku: str) -> str:
    item_dir = ensure_item_dir(sku)
    qr_img = qrcode.make(f"/item/{sku}")
    qr_path = item_dir / "qr.png"
    qr_img.save(qr_path)
    return str(qr_path)


def log_activity(db: Session, item_id: int | None, action: str, details: str = "") -> None:
    db.add(models.ActivityLog(item_id=item_id, action=action, details=details, user="system"))
    db.commit()


def listing_generator(title: str, category: str | None, condition: str | None, photos: list[str], price: float):
    keywords = [word.lower() for word in title.split() if len(word) > 2][:8]
    generated_title = f"{title} | {condition or 'Good'} | {category or 'General'}"
    generated_description = (
        f"{title}\n"
        f"Category: {category or 'General'}\n"
        f"Condition: {condition or 'Not specified'}\n"
        f"Includes {len(photos)} photo(s).\n"
        f"Price: ${price:.2f}"
    )
    return {
        "generated_title": generated_title[:80],
        "generated_description": generated_description,
        "keywords": keywords,
    }
