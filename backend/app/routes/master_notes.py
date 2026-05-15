from fastapi import APIRouter, HTTPException
from app.database import get_db

router = APIRouter(prefix="/api/master-notes", tags=["Master Notes"])


@router.get("/subjects")
async def get_subjects():
    """Return list of all available master note subjects."""
    db = get_db()
    subjects = await db.master_notes.distinct("subject")
    return sorted(subjects)


@router.get("/subject/{subject}")
async def get_subject_content(subject: str):
    """Return full content of a master note by subject name."""
    db = get_db()
    doc = await db.master_notes.find_one({"subject": subject})
    if not doc:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {
        "id": str(doc["_id"]),
        "subject": doc["subject"],
        "content": doc["content"],
    }
