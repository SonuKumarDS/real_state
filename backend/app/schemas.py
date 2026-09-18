from pydantic import BaseModel, ConfigDict
from typing import Optional

class PropertyIn(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str = ""
    property_type: str = "Unknown"
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    sqft: Optional[int] = None
    lot_size: Optional[float] = None
    year_built: Optional[int] = None
    asking_price: Optional[float] = None
    listing_status: str = "Unknown"
    source: str = "Manual"
    source_url: str = ""
    verification_status: str = "UNVERIFIED"
    notes: str = ""

class InvestorIn(BaseModel):
    name: str
    company: str = ""
    location: str = ""
    email: str = ""
    phone: str = ""
    website: str = ""
    source: str = "Manual"
    strategies: str = ""
    property_types: str = ""
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    cash_buyer: bool = False
    verification_status: str = "UNVERIFIED"
    notes: str = ""

class DealIn(BaseModel):
    property_id: int
    investor_id: int
    status: str = "LEAD"
    offer_amount: Optional[float] = None
    commission_amount: Optional[float] = None
    commission_status: str = "PENDING"
    closing_date: str = ""
    notes: str = ""

class MatchOut(BaseModel):
    id: int
    property_id: int
    investor_id: int
    score: float
    reasons: str
    concerns: str
    status: str
    model_config = ConfigDict(from_attributes=True)
