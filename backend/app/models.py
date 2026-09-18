from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

def now():
    return datetime.now(timezone.utc)

from .database import Base

class Property(Base):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(300), index=True)
    city: Mapped[str] = mapped_column(String(100), index=True)
    state: Mapped[str] = mapped_column(String(100), index=True)
    zip_code: Mapped[str] = mapped_column(String(20), default="")
    property_type: Mapped[str] = mapped_column(String(80), default="Unknown")
    bedrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[float | None] = mapped_column(Float, nullable=True)
    sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lot_size: Mapped[float | None] = mapped_column(Float, nullable=True)
    year_built: Mapped[int | None] = mapped_column(Integer, nullable=True)
    asking_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    listing_status: Mapped[str] = mapped_column(String(50), default="Unknown")
    source: Mapped[str] = mapped_column(String(100), default="Manual")
    source_url: Mapped[str] = mapped_column(String(1000), default="")
    verification_status: Mapped[str] = mapped_column(String(40), default="UNVERIFIED")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)

class Investor(Base):
    __tablename__ = "investors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    company: Mapped[str] = mapped_column(String(200), default="")
    location: Mapped[str] = mapped_column(String(200), default="")
    email: Mapped[str] = mapped_column(String(300), default="")
    phone: Mapped[str] = mapped_column(String(60), default="")
    website: Mapped[str] = mapped_column(String(1000), default="")
    source: Mapped[str] = mapped_column(String(100), default="Manual")
    strategies: Mapped[str] = mapped_column(String(500), default="")
    property_types: Mapped[str] = mapped_column(String(500), default="")
    min_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    cash_buyer: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_status: Mapped[str] = mapped_column(String(40), default="UNVERIFIED")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)

class Match(Base):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), index=True)
    investor_id: Mapped[int] = mapped_column(ForeignKey("investors.id"), index=True)
    score: Mapped[float] = mapped_column(Float)
    reasons: Mapped[str] = mapped_column(Text, default="")
    concerns: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(50), default="NEW")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Deal(Base):
    __tablename__ = "deals"
    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    investor_id: Mapped[int] = mapped_column(ForeignKey("investors.id"))
    status: Mapped[str] = mapped_column(String(50), default="LEAD")
    offer_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    commission_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    commission_status: Mapped[str] = mapped_column(String(50), default="PENDING")
    closing_date: Mapped[str] = mapped_column(String(30), default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(100))
    entity: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[str] = mapped_column(String(100), default="")
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
