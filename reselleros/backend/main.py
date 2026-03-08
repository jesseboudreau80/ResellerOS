import threading
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func

from . import models
from .database import Base, SessionLocal, engine
from .routes import barcode, items, marketplace, qr, warehouse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ResellerOS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
app.include_router(warehouse.router)
app.include_router(marketplace.router)
app.include_router(qr.router)
app.include_router(barcode.router)


@app.get("/dashboard")
def dashboard():
    db = SessionLocal()
    try:
        total_inventory = db.query(models.Item).count()
        items_listed = db.query(models.Item).filter(models.Item.status == "listed").count()
        items_sold = db.query(models.Item).filter(models.Item.status == "sold").count()
        inventory_value = db.query(func.sum(models.Item.price)).scalar() or 0
        profit = db.query(func.sum(models.Item.profit)).scalar() or 0
        return {
            "total_inventory": total_inventory,
            "items_listed": items_listed,
            "items_sold": items_sold,
            "inventory_value": inventory_value,
            "profit": profit,
        }
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


def worker_loop():
    while True:
        db = SessionLocal()
        try:
            job = (
                db.query(models.Job)
                .filter(models.Job.status == "queued")
                .order_by(models.Job.created_at.asc())
                .first()
            )
            if not job:
                time.sleep(1)
                continue
            job.status = "processing"
            job.attempts += 1
            db.commit()
            try:
                marketplace.process_job(db, job)
                db.commit()
            except Exception as exc:  # noqa: BLE001
                job.status = "failed"
                job.error_message = str(exc)
                db.commit()
        finally:
            db.close()


worker_thread = threading.Thread(target=worker_loop, daemon=True)
worker_thread.start()
