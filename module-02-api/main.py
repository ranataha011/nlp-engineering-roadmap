from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import models
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import Header, HTTPException

API_KEY = "supersecret123"


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
class LeadSchema(BaseModel):
    business_name: str
    category: str
    has_website: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello, this is my first API"}


@app.get("/leads")
def get_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).all()


@app.post("/leads")
def create_lead(lead: LeadSchema, db: Session = Depends(get_db), auth=Depends(verify_api_key) ):
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


@app.get("/leads/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead:
        return lead
    return {"error": "Lead not found"}
@app.put("/leads/{lead_id}")
def update_lead(lead_id: int, lead: LeadSchema, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        return {"error": "Lead not found"}
    db_lead.business_name = lead.business_name
    db_lead.category = lead.category
    db_lead.has_website = lead.has_website
    db.commit()
    db.refresh(db_lead)
    return db_lead


@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        return {"error": "Lead not found"}
    db.delete(db_lead)
    db.commit()
    return {"message": f"Lead {lead_id} deleted"}
