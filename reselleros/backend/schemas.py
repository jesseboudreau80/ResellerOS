from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    title: str = "New Item"
    description: str = ""
    category: Optional[str] = None
    condition: Optional[str] = None
    price: float = 0.0
    cost: float = 0.0
    barcode: Optional[str] = None
    barcode_type: Optional[str] = None
    shelf_location: Optional[str] = None


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    shelf_location: Optional[str] = None
    status: Optional[str] = None


class ItemOut(BaseModel):
    sku: str
    title: str
    description: str
    price: float
    cost: float
    profit: float
    barcode: str
    barcode_type: str
    shelf_location: Optional[str]
    status: str
    date_added: datetime

    class Config:
        from_attributes = True


class QuickAddBatch(BaseModel):
    count: int


class MoveItemRequest(BaseModel):
    location_code: str


class MarketplaceRequest(BaseModel):
    sku: str


class ListingGeneratorInput(BaseModel):
    title: str
    category: Optional[str] = None
    condition: Optional[str] = None
    photos: List[str] = Field(default_factory=list)
    price: float


class AuctionBase(BaseModel):
    platform: str
    facility_name: str
    city: Optional[str] = None
    unit_id: str
    unit_size: Optional[str] = None
    auction_end_date: Optional[datetime] = None
    listing_url: Optional[str] = None
    photo_quality: Optional[str] = None
    deal_score: float = 0.0
    confidence_rating: float = 0.0
    anchor_item: Optional[str] = None
    estimated_resale_min: float = 0.0
    estimated_resale_max: float = 0.0
    organization_level: Optional[str] = None
    packing_density: Optional[str] = None
    locker_type: Optional[str] = None
    claude_analysis_notes: Optional[str] = None
    safe_bid: float = 0.0
    target_bid: float = 0.0
    max_bid: float = 0.0
    opening_bid: float = 0.0
    current_bid: float = 0.0
    bid_status: str = "watching"
    bid_timestamp: Optional[datetime] = None
    final_sale_price: float = 0.0
    did_win: bool = False
    overbid_amount: float = 0.0
    competition_level: Optional[str] = None
    purchase_price: float = 0.0
    buyer_premium: float = 0.0
    pickup_cost: float = 0.0
    dump_cost: float = 0.0
    total_cost: float = 0.0
    total_revenue: float = 0.0
    profit: float = 0.0
    roi_percent: float = 0.0
    claude_accuracy_rating: float = 0.0
    hidden_items_found: int = 0
    facility_rating: float = 0.0
    would_buy_again: bool = False


class AuctionCreate(AuctionBase):
    pass


class AuctionUpdate(BaseModel):
    platform: Optional[str] = None
    facility_name: Optional[str] = None
    city: Optional[str] = None
    unit_id: Optional[str] = None
    bid_status: Optional[str] = None
    current_bid: Optional[float] = None
    did_win: Optional[bool] = None
    final_sale_price: Optional[float] = None
    total_revenue: Optional[float] = None
    purchase_price: Optional[float] = None
    buyer_premium: Optional[float] = None
    pickup_cost: Optional[float] = None
    dump_cost: Optional[float] = None
    locker_type: Optional[str] = None
    facility_rating: Optional[float] = None


class AuctionOut(AuctionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AuctionToInventory(BaseModel):
    count: int = 1
    title_prefix: str = "Auction Item"
