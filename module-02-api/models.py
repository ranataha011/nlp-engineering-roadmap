from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, index=True)
    category = Column(String)
    has_website = Column(Boolean)
