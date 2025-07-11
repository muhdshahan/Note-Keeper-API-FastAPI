# Defines the note table structure used in database

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Note(Base):
    __tablename__ = "notes"
    
    # each attribute maps to a column in the notes table
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    tag = Column(String, nullable=True)  # optional as nullable = True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # createdat automatically set using serverdefault=func.now() so DB autogenerates timestamp
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)