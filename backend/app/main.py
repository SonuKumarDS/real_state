import csv, io, json
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from .config import settings
from .database import Base, engine, get_db
from .models import Property, Investor, Match, Deal, AuditLog
from .schemas import PropertyIn, InvestorIn, DealIn, MatchOut
from .matching import match_property_investor

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def audit(db, action, entity, entity_id="", details=""):
    db.add(AuditLog(action=action, entity=entity, entity_id=str(entity_id), details=details))
    db.commit()

@app.get("/api/health")
def health():
    return {"status": "ok", "service": settings.app_name}

@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return {
        "properties": db.query(Property).count(),
        "investors": db.query(Investor).count(),
        "matches": db.query(Match).count(),
        "deals": db.query(Deal).count(),
        "potential_commission": db.query(func.coalesce(func.sum(Deal.commission_amount), 0)).scalar() or 0,
        "received_commission": db.query(func.coalesce(func.sum(Deal.commission_amount), 0)).filter(Deal.commission_status=="RECEIVED").scalar() or 0,
    }

@app.get("/api/properties")
def properties(db: Session = Depends(get_db), q: str = "", limit: int = Query(100, le=500)):
    query = db.query(Property)
    if q:
        term = f"%{q}%"
        query = query.filter((Property.address.ilike(term)) | (Property.city.ilike(term)) | (Property.state.ilike(term)))
    return query.order_by(Property.id.desc()).limit(limit).all()

@app.post("/api/properties")
def create_property(data: PropertyIn, db: Session = Depends(get_db)):
    obj = Property(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    audit(db, "CREATE", "property", obj.id, data.model_dump_json())
    return obj

@app.get("/api/properties/{property_id}")
def get_property(property_id: int, db: Session = Depends(get_db)):
    obj = db.get(Property, property_id)
    if not obj: raise HTTPException(404, "Property not found")
    return obj

@app.get("/api/investors")
def investors(db: Session = Depends(get_db), q: str = "", limit: int = Query(100, le=500)):
    query = db.query(Investor)
    if q:
        term = f"%{q}%"
        query = query.filter((Investor.name.ilike(term)) | (Investor.company.ilike(term)) | (Investor.location.ilike(term)))
    return query.order_by(Investor.id.desc()).limit(limit).all()

@app.post("/api/investors")
def create_investor(data: InvestorIn, db: Session = Depends(get_db)):
    obj = Investor(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    audit(db, "CREATE", "investor", obj.id, data.model_dump_json())
    return obj

@app.post("/api/import/properties")
async def import_properties(file: UploadFile = File(...), db: Session = Depends(get_db)):
    raw = await file.read()
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    created = 0
    for r in rows:
        if not r.get("address") or not r.get("city") or not r.get("state"):
            continue
        obj = Property(
            address=r["address"], city=r["city"], state=r["state"],
            zip_code=r.get("zip_code",""), property_type=r.get("property_type","Unknown"),
            bedrooms=int(r["bedrooms"]) if r.get("bedrooms") else None,
            bathrooms=float(r["bathrooms"]) if r.get("bathrooms") else None,
            sqft=int(r["sqft"]) if r.get("sqft") else None,
            asking_price=float(r["asking_price"]) if r.get("asking_price") else None,
            source=r.get("source","CSV"), source_url=r.get("source_url",""),
            verification_status=r.get("verification_status","UNVERIFIED"),
            notes=r.get("notes","")
        )
        db.add(obj); created += 1
    db.commit()
    audit(db, "IMPORT", "properties", "", f"created={created}")
    return {"created": created, "rows": len(rows)}

@app.post("/api/import/investors")
async def import_investors(file: UploadFile = File(...), db: Session = Depends(get_db)):
    raw = await file.read()
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    created = 0
    for r in rows:
        if not r.get("name"):
            continue
        obj = Investor(
            name=r["name"], company=r.get("company",""), location=r.get("location",""),
            email=r.get("email",""), phone=r.get("phone",""), website=r.get("website",""),
            source=r.get("source","CSV"), strategies=r.get("strategies",""),
            property_types=r.get("property_types",""),
            min_price=float(r["min_price"]) if r.get("min_price") else None,
            max_price=float(r["max_price"]) if r.get("max_price") else None,
            cash_buyer=str(r.get("cash_buyer","")).lower() in ("1","true","yes"),
            verification_status=r.get("verification_status","UNVERIFIED"), notes=r.get("notes","")
        )
        db.add(obj); created += 1
    db.commit()
    audit(db, "IMPORT", "investors", "", f"created={created}")
    return {"created": created, "rows": len(rows)}

@app.post("/api/matches/generate")
def generate_matches(property_id: int | None = None, investor_id: int | None = None, db: Session = Depends(get_db)):
    props = [db.get(Property, property_id)] if property_id else db.query(Property).all()
    invs = [db.get(Investor, investor_id)] if investor_id else db.query(Investor).all()
    props = [p for p in props if p]
    invs = [i for i in invs if i]
    created = 0
    for p in props:
        for i in invs:
            score, reasons, concerns = match_property_investor(p, i)
            if score < 40: continue
            exists = db.query(Match).filter(Match.property_id==p.id, Match.investor_id==i.id).first()
            if exists:
                exists.score, exists.reasons, exists.concerns = score, "; ".join(reasons), "; ".join(concerns)
            else:
                db.add(Match(property_id=p.id, investor_id=i.id, score=score,
                             reasons="; ".join(reasons), concerns="; ".join(concerns)))
                created += 1
    db.commit()
    audit(db, "GENERATE", "matches", "", f"created={created}")
    return {"created": created}

@app.get("/api/matches", response_model=list[MatchOut])
def matches(db: Session = Depends(get_db), limit: int = Query(100, le=500)):
    return db.query(Match).order_by(Match.score.desc()).limit(limit).all()

@app.post("/api/deals")
def create_deal(data: DealIn, db: Session = Depends(get_db)):
    if not db.get(Property, data.property_id) or not db.get(Investor, data.investor_id):
        raise HTTPException(400, "Property and investor must exist")
    obj = Deal(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    audit(db, "CREATE", "deal", obj.id, data.model_dump_json())
    return obj

@app.get("/api/deals")
def deals(db: Session = Depends(get_db)):
    return db.query(Deal).order_by(Deal.id.desc()).all()

@app.get("/api/audit")
def audit_logs(db: Session = Depends(get_db), limit: int = Query(100, le=500)):
    return db.query(AuditLog).order_by(AuditLog.id.desc()).limit(limit).all()
