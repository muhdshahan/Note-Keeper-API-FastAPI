from fastapi import APIRouter, Depends, HTTPException,Request  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.limiter import limiter
from app.db.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate, NoteOut
from app.dependencies.auth import get_current_user
from app.models.user import User
import logging

router = APIRouter(prefix="/notes", tags=["Notes"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=NoteOut)
async def create_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_note = Note(**note.dict(), owner_id=current_user.id)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    logger.info(f"Note created by {current_user.username}")
    return db_note

@router.get("/", response_model=List[NoteOut])
@limiter.limit("5/minute")
async def get_notes(
    request: Request, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        result = await db.execute(select(Note))
    else:
        result = await db.execute(select(Note).where(Note.owner_id == current_user.id))
        notes = result.scalars().all()
    return notes

@router.get("/{note_id}", response_model=NoteOut)
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Note).where(Note.id == note_id))
    note = result.scalar_one_or_none()
    if not note or (note.owner_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to view this note")
    return note

@router.put("/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Note).where(Note.id == note_id))
    db_note = result.scalar_one_or_none()
    if not db_note or (db_note.owner_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to update this note")

    for key, value in note_data.dict().items():
        setattr(db_note, key, value)
    await db.commit()
    await db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Note).where(Note.id == note_id))
    db_note = result.scalar_one_or_none()
    if not db_note or (db_note.owner_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")

    await db.delete(db_note)
    await db.commit()
    return {"message": "Note deleted successfully"}
