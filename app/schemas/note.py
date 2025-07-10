# Defines structure of data sent to and returned from API using Pydantic models

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# NoteBase holds common fields shared between create, update and output
class NoteBase(BaseModel):
    title: str
    content: str
    tag: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True