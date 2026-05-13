from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import get_db

router = APIRouter(prefix="/api/detailed-study", tags=["Detailed Study"])


def doc_helper(d) -> dict:
    return {
        "id": str(d["_id"]),
        "subject": d["subject"],
        "content": d["content"],
    }


@router.get("/subjects")
async def get_subjects():
    db = get_db()
    subjects = await db.master_notes.distinct("subject")
    return sorted(subjects)


@router.get("/subject/{subject}")
async def get_by_subject(subject: str):
    db = get_db()
    doc = await db.master_notes.find_one({"subject": subject})
    if not doc:
        raise HTTPException(status_code=404, detail="Subject not found")
    return doc_helper(doc)


@router.get("/search")
async def search_notes(q: str = ""):
    if not q or len(q) < 2:
        return []
    db = get_db()
    cursor = db.master_notes.find(
        {"content": {"$regex": q, "$options": "i"}},
        {"subject": 1},
    )
    results = []
    async for doc in cursor:
        results.append({"id": str(doc["_id"]), "subject": doc["subject"]})
    return results
