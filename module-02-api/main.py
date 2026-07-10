from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Lead(BaseModel):
    id: int
    business_name: str
    category: str
    has_website: bool


leads: list[Lead] = []


@app.get("/")
def read_root():
    return {"message": "Hello, this is my first API"}


@app.get("/leads")
def get_leads():
    return leads


@app.post("/leads")
def create_lead(lead: Lead):
    leads.append(lead)
    return lead
@app.get("/leads/{lead_id}")
def get_lead(lead_id: int):
    for lead in leads:
        if lead.id == lead_id:
            return lead
    return {"error": "Lead not found"}
