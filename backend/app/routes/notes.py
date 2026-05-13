from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from datetime import datetime
from app.database import get_db
from app.models import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/api/notes", tags=["Notes"])


def note_helper(n) -> dict:
    return {
        "id": str(n["_id"]),
        "subject": n["subject"],
        "chapter": n.get("chapter", ""),
        "full_notes": n.get("full_notes", ""),
        "mnemonics": n.get("mnemonics", ""),
        "clinical_concepts": n.get("clinical_concepts", ""),
        "mcqs": n.get("mcqs", ""),
        "rapid_revision": n.get("rapid_revision", ""),
        "created_at": n["created_at"],
        "updated_at": n.get("updated_at", n["created_at"]),
    }


@router.post("/", response_model=NoteResponse, status_code=201)
async def create_note(note: NoteCreate):
    db = get_db()
    doc = note.model_dump()
    now = datetime.utcnow()
    doc["created_at"] = now
    doc["updated_at"] = now
    result = await db.notes.insert_one(doc)
    created = await db.notes.find_one({"_id": result.inserted_id})
    return note_helper(created)


@router.get("/", response_model=list[NoteResponse])
async def get_notes(
    subject: str | None = None,
    topic: str | None = None,
    chapter: str | None = None,
    search: str | None = None,
    limit: int = Query(default=50, le=200),
    skip: int = 0,
):
    db = get_db()
    query = {}
    if subject:
        query["subject"] = subject
    if topic:
        query["chapter"] = topic
    if chapter:
        query["chapter"] = chapter
    if search:
        query["$or"] = [
            {"chapter": {"$regex": search, "$options": "i"}},
            {"full_notes": {"$regex": search, "$options": "i"}},
        ]

    cursor = db.notes.find(query).sort("updated_at", -1).skip(skip).limit(limit)
    notes = []
    async for n in cursor:
        notes.append(note_helper(n))
    return notes


@router.get("/subjects")
async def get_note_subjects():
    db = get_db()
    subjects = await db.notes.distinct("subject")
    return subjects


@router.get("/chapters/{subject}")
async def get_note_chapters(subject: str):
    db = get_db()
    chapters = await db.notes.distinct("chapter", {"subject": subject})
    return chapters


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str):
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")
    db = get_db()
    note = await db.notes.find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note_helper(note)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, note: NoteUpdate):
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")
    db = get_db()
    update_data = {k: v for k, v in note.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    update_data["updated_at"] = datetime.utcnow()

    result = await db.notes.update_one(
        {"_id": ObjectId(note_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    updated = await db.notes.find_one({"_id": ObjectId(note_id)})
    return note_helper(updated)


@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: str):
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")
    db = get_db()
    result = await db.notes.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
