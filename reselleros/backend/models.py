from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class ShippingProfile(Base):
    __tablename__ = "shipping_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    carrier = Column(String, nullable=False)
    service = Column(String, nullable=False)
    handling_time = Column(Integer, default=1)
    cost_type = Column(String, default="flat")
    flat_rate_cost = Column(Float, default=0.0)
    international_enabled = Column(Boolean, default=False)
    marketplace_policy_id = Column(String, nullable=True)


class PaymentProfile(Base):
    __tablename__ = "payment_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    payment_method = Column(String, nullable=False)
    marketplace_policy_id = Column(String, nullable=True)


class ReturnProfile(Base):
    __tablename__ = "return_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    return_days = Column(Integer, default=30)
    return_shipping_paid_by = Column(String, default="buyer")
    marketplace_policy_id = Column(String, nullable=True)


class WarehouseLocation(Base):
    __tablename__ = "warehouse_locations"

    id = Column(Integer, primary_key=True, index=True)
    location_code = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, nullable=False, unique=True, index=True)
    barcode = Column(String, nullable=False)
    barcode_type = Column(String, nullable=False, default="CODE128")
    title = Column(String, default="New Item")
    description = Column(Text, default="")
    category = Column(String, nullable=True)
    condition = Column(String, nullable=True)
    price = Column(Float, default=0.0)
    cost = Column(Float, default=0.0)
    weight = Column(Float, nullable=True)
    dimensions = Column(String, nullable=True)
    shelf_location = Column(String, nullable=True)
    shipping_profile_id = Column(Integer, ForeignKey("shipping_profiles.id"), nullable=True)
    payment_profile_id = Column(Integer, ForeignKey("payment_profiles.id"), nullable=True)
    return_profile_id = Column(Integer, ForeignKey("return_profiles.id"), nullable=True)
    status = Column(String, default="available")
    date_added = Column(DateTime, default=datetime.utcnow)
    date_sold = Column(DateTime, nullable=True)
    profit = Column(Float, default=0.0)

    ebay_listing_id = Column(String, nullable=True)
    ebay_url = Column(String, nullable=True)
    facebook_url = Column(String, nullable=True)
    mercari_url = Column(String, nullable=True)
    website_url = Column(String, nullable=True)

    photos = relationship("Photo", back_populates="item", cascade="all, delete-orphan")


class MarketplaceLink(Base):
    __tablename__ = "marketplace_links"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    marketplace = Column(String, nullable=False)
    listing_id = Column(String, nullable=True)
    url = Column(String, nullable=True)


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    file_path = Column(String, nullable=False)

    item = relationship("Item", back_populates="photos")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=True)
    action = Column(String, nullable=False)
    user = Column(String, default="system")
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(Text, nullable=True)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    action = Column(String, nullable=False)
    status = Column(String, default="queued")
    attempts = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
