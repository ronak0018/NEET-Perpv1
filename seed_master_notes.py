"""
Seed master notes from Files/Master-notes/ into MongoDB master_notes collection.
Deduplicates .md/.txt — prefers .md if both exist for same subject.
"""
import os
import re
import asyncio
import certifi
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb+srv://ronakmeandeveloper_db_user:OtNMxQE3DdzdWwyo@cluster0.ic6ndjr.mongodb.net/"
)
DATABASE_NAME = os.getenv("DATABASE_NAME", "neetpg")
NOTES_DIR = os.path.join(os.path.dirname(__file__), "Files", "Master-notes")

SUBJECT_MAP = {
    "anatomy": "Anatomy",
    "surgery": "Surgery",
    "radiology": "Radiology",
    "psychiatry": "Psychiatry",
    "anaesthesia_neet_pg_study_notes": "Anaesthesia",
    "physiology_neet_pg_study_notes": "Physiology",
    "pharmacology_neet_pg_study_notes": "Pharmacology",
}


def extract_subject(filename: str) -> str:
    stem = re.sub(r"\.(md|txt)$", "", filename.lower())
    return SUBJECT_MAP.get(stem, stem.replace("_", " ").title())


async def seed():
    client = AsyncIOMotorClient(MONGODB_URL, tlsCAFile=certifi.where())
    db = client[DATABASE_NAME]

    deleted = await db.master_notes.delete_many({})
    print(f"Cleared {deleted.deleted_count} existing master notes.")

    # Collect files, prefer .md over .txt for same subject
    files_by_subject: dict[str, str] = {}
    for fname in sorted(os.listdir(NOTES_DIR)):
        if not (fname.endswith(".txt") or fname.endswith(".md")):
            continue
        subject = extract_subject(fname)
        path = os.path.join(NOTES_DIR, fname)
        if subject in files_by_subject:
            # prefer .md
            if fname.endswith(".md"):
                files_by_subject[subject] = path
        else:
            files_by_subject[subject] = path

    docs = []
    for subject, path in sorted(files_by_subject.items()):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        docs.append({"subject": subject, "content": content})
        print(f"  {subject}: {os.path.basename(path)} ({len(content):,} chars)")

    if docs:
        result = await db.master_notes.insert_many(docs)
        print(f"\nTotal: {len(result.inserted_ids)} subjects seeded into '{DATABASE_NAME}.master_notes'")
    else:
        print("No files found.")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
