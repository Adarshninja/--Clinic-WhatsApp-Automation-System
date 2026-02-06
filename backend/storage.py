import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "leads.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String)
    date = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ----------------------------
# Shared user state (demo-safe)
# ----------------------------
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "user_id": user_id,
            "step": "WELCOME",
            "service": None,
            "date": None,
            "phone": None
        }
    return users[user_id]

def save_user(user):
    users[user["user_id"]] = user

def save_lead(user):
    db = SessionLocal()
    lead = Lead(
        service=user["service"],
        date=user["date"],
        phone=user["phone"]
    )
    db.add(lead)
    db.commit()
    db.close()

def get_all_leads():
    db = SessionLocal()
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    db.close()
    return leads
# updated state

def delete_lead(lead_id: int):
    db = SessionLocal()
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead:
        db.delete(lead)
        db.commit()
    db.close()


def export_leads_as_dict():
    db = SessionLocal()
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    db.close()

    return [
        {
            "ID": lead.id,
            "Service": lead.service,
            "Date": lead.date,
            "Phone": lead.phone,
            "Received At": lead.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for lead in leads
    ]
