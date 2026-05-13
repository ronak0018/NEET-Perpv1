"""
Seed study notes from Files/study_notes/*.json into MongoDB notes collection.
"""
import os
import json
import asyncio
import certifi
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb+srv://ronakmeandeveloper_db_user:OtNMxQE3DdzdWwyo@cluster0.ic6ndjr.mongodb.net/"
)
DATABASE_NAME = os.getenv("DATABASE_NAME", "neetpg")
NOTES_DIR = os.path.join(os.path.dirname(__file__), "Files", "study_notes")


async def seed():
    client = AsyncIOMotorClient(MONGODB_URL, tlsCAFile=certifi.where())
    db = client[DATABASE_NAME]

    # Clear existing notes
    deleted = await db.notes.delete_many({})
    print(f"Cleared {deleted.deleted_count} existing notes.")

    total = 0
    for filename in sorted(os.listdir(NOTES_DIR)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(NOTES_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            chapters = json.load(f)

        docs = []
        now = datetime.utcnow()
        for ch in chapters:
            docs.append({
                "subject": ch["subject"],
                "chapter": ch["chapter"],
                "full_notes": ch.get("full_notes", ""),
                "mnemonics": ch.get("mnemonics", ""),
                "clinical_concepts": ch.get("clinical_concepts", ""),
                "mcqs": ch.get("mcqs", ""),
                "rapid_revision": ch.get("rapid_revision", ""),
                "created_at": now,
                "updated_at": now,
            })

        if docs:
            result = await db.notes.insert_many(docs)
            count = len(result.inserted_ids)
            total += count
            print(f"  {filename}: {count} chapters seeded")

    print(f"\nTotal: {total} notes seeded into '{DATABASE_NAME}.notes'")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
