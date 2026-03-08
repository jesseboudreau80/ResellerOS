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
