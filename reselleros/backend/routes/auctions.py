from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas, services
from ..database import get_db

router = APIRouter(prefix="/auctions", tags=["auctions"])


def recalc(auction: models.AuctionTracker):
    auction.total_cost = (auction.purchase_price or 0) + (auction.buyer_premium or 0) + (auction.pickup_cost or 0) + (auction.dump_cost or 0)
    auction.profit = (auction.total_revenue or 0) - (auction.total_cost or 0)
    auction.roi_percent = ((auction.profit / auction.total_cost) * 100) if auction.total_cost else 0


@router.post("", response_model=schemas.AuctionOut)
def create_auction(payload: schemas.AuctionCreate, db: Session = Depends(get_db)):
    auction = models.AuctionTracker(**payload.model_dump())
    recalc(auction)
    db.add(auction)
    db.commit()
    db.refresh(auction)
    return auction


@router.get("/active", response_model=list[schemas.AuctionOut])
def active_auctions(db: Session = Depends(get_db)):
    return (
        db.query(models.AuctionTracker)
        .filter(models.AuctionTracker.bid_status.in_(["watching", "bidding", "won"]))
        .order_by(models.AuctionTracker.auction_end_date.asc())
        .all()
    )


@router.get("/history", response_model=list[schemas.AuctionOut])
def auction_history(db: Session = Depends(get_db)):
    return (
        db.query(models.AuctionTracker)
        .filter(models.AuctionTracker.bid_status.in_(["won", "lost", "overbid", "closed"]))
        .order_by(models.AuctionTracker.created_at.desc())
        .all()
    )


@router.get("/analytics")
def auction_analytics(db: Session = Depends(get_db)):
    total = db.query(models.AuctionTracker).count()
    wins = db.query(models.AuctionTracker).filter(models.AuctionTracker.did_win.is_(True)).count()
    avg_roi = db.query(func.avg(models.AuctionTracker.roi_percent)).scalar() or 0
    avg_bid = db.query(func.avg(models.AuctionTracker.max_bid)).scalar() or 0
    avg_resale = db.query(func.avg(models.AuctionTracker.total_revenue)).scalar() or 0

    facility_rows = (
        db.query(models.AuctionTracker.facility_name, func.avg(models.AuctionTracker.roi_percent))
        .group_by(models.AuctionTracker.facility_name)
        .all()
    )
    locker_rows = (
        db.query(models.AuctionTracker.locker_type, func.avg(models.AuctionTracker.roi_percent))
        .group_by(models.AuctionTracker.locker_type)
        .all()
    )

    return {
        "win_rate": (wins / total * 100) if total else 0,
        "average_roi": avg_roi,
        "average_bid": avg_bid,
        "average_resale": avg_resale,
        "roi_by_facility": [{"facility": f or "Unknown", "roi": r or 0} for f, r in facility_rows],
        "roi_by_locker_type": [{"locker_type": l or "Unknown", "roi": r or 0} for l, r in locker_rows],
    }


@router.put("/{auction_id}", response_model=schemas.AuctionOut)
def update_auction(auction_id: int, payload: schemas.AuctionUpdate, db: Session = Depends(get_db)):
    auction = db.query(models.AuctionTracker).filter(models.AuctionTracker.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(auction, key, value)
    recalc(auction)
    db.commit()
    db.refresh(auction)
    return auction


@router.post("/{auction_id}/intake")
def auction_to_intake(auction_id: int, payload: schemas.AuctionToInventory, db: Session = Depends(get_db)):
    auction = db.query(models.AuctionTracker).filter(models.AuctionTracker.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if not auction.did_win:
        raise HTTPException(status_code=400, detail="Only won auctions can be added to intake")

    created = []
    for i in range(payload.count):
        sku = services.generate_sku(db)
        item = models.Item(
            sku=sku,
            barcode=sku,
            barcode_type="CODE128",
            title=f"{payload.title_prefix} {i + 1}",
            description=f"From auction #{auction.id} at {auction.facility_name}",
            cost=(auction.total_cost or 0) / max(payload.count, 1),
            price=0,
            shelf_location="INTAKE",
            status="available",
            profit=0,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        services.generate_barcode_image(item.sku, item.sku)
        services.generate_qr_image(item.sku)
        created.append({"sku": item.sku, "title": item.title})
    return {"created": created, "count": len(created)}
