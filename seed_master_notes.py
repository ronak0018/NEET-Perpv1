"""
Seed master notes from Files/Master-notes/ and Files/Files/ into MongoDB master_notes collection.
Prefers Master-notes .md > Master-notes .txt > Files/Files/ .txt.
Covers all 19+ medical subjects for NEET PG.
"""
import os
import re
import asyncio
import certifi
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load .env from backend/
load_dotenv(Path(__file__).resolve().parent / "backend" / ".env")

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "neetpg")

BASE_DIR = Path(__file__).resolve().parent
MASTER_NOTES_DIR = BASE_DIR / "Files" / "Master-notes"
FILES_DIR = BASE_DIR / "Files" / "Files"

# Map filename stems -> clean subject names
FILENAME_TO_SUBJECT = {
    # Master-notes folder
    "anaesthesia_neet_pg_study_notes": "Anaesthesia",
    "anatomy": "Anatomy",
    "dermatology_neet_pg_complete_study_notes": "Dermatology",
    "ent_neet_pg_study_notes": "ENT",
    "forensic_medicine_neet_pg_detailed_notes": "Forensic Medicine",
    "neet_pg_biochemistry_study_pack": "Biochemistry",
    "neet_pg_medicine_complete_study_notes": "Medicine",
    "paediatrics_neet_pg_notes": "Paediatrics",
    "pathology_neet_pg_high_yield_notes": "Pathology",
    "pharmacology_neet_pg_study_notes": "Pharmacology",
    "physiology_neet_pg_study_notes": "Physiology",
    "psm_neet_pg_high_yield_notes_2026": "PSM",
    "psychiatry": "Psychiatry",
    "radiology": "Radiology",
    "surgery": "Surgery",
    # Files/Files folder
    "complete_anaesthesia_neetpg_notes": "Anaesthesia",
    "complete_anatomy_neetpg_notes": "Anatomy",
    "complete_biochemistry_neetpg_notes": "Biochemistry",
    "complete_dermatology_neetpg_notes": "Dermatology",
    "complete_ent_neetpg_notes": "ENT",
    "complete_forensic_medicine_neetpg_notes": "Forensic Medicine",
    "complete_microbiology_neetpg_notes": "Microbiology",
    "complete_obg_neetpg_notes": "OBG",
    "complete_ophthalmology_neetpg_notes": "Ophthalmology",
    "complete_orthopaedics_neetpg_notes": "Orthopaedics",
    "complete_pathology_neetpg_notes": "Pathology",
    "complete_pharmacology_neetpg_notes": "Pharmacology",
    "complete_physiology_neetpg_notes": "Physiology",
    "complete_psm_neetpg_notes": "PSM",
    "complete_psychiatry_neetpg_notes": "Psychiatry",
    "complete_radiology_neetpg_notes": "Radiology",
    "complete_surgery_neetpg_notes": "Surgery",
    "brachial_plexus_master_notes_neetpg": "Brachial Plexus",
}


def get_subject(filepath: Path) -> str:
    stem = filepath.stem.lower()
    return FILENAME_TO_SUBJECT.get(stem, stem.replace("_", " ").title())


async def seed():
    client = AsyncIOMotorClient(MONGODB_URL, tlsCAFile=certifi.where())
    db = client[DATABASE_NAME]

    deleted = await db.master_notes.delete_many({})
    print(f"Cleared {deleted.deleted_count} existing master notes.")

    # Priority: Master-notes .md > Master-notes .txt > Files/Files .txt
    # Collect all candidates grouped by subject
    files_by_subject: dict[str, tuple[Path, int]] = {}  # subject -> (path, priority)

    # Pass 1: Master-notes folder (priority 1 for .md, 2 for .txt)
    if MASTER_NOTES_DIR.exists():
        for f in sorted(MASTER_NOTES_DIR.iterdir()):
            if f.suffix not in (".md", ".txt"):
                continue
            subject = get_subject(f)
            priority = 1 if f.suffix == ".md" else 2
            if subject not in files_by_subject or priority < files_by_subject[subject][1]:
                files_by_subject[subject] = (f, priority)

    # Pass 2: Files/Files folder (priority 3 — only if not already from Master-notes)
    if FILES_DIR.exists():
        for f in sorted(FILES_DIR.iterdir()):
            if f.suffix not in (".md", ".txt"):
                continue
            subject = get_subject(f)
            if subject not in files_by_subject:
                files_by_subject[subject] = (f, 3)

    docs = []
    for subject in sorted(files_by_subject.keys()):
        path, _ = files_by_subject[subject]
        content = path.read_text(encoding="utf-8")
        docs.append({"subject": subject, "content": content})
        print(f"  {subject}: {path.name} ({len(content):,} chars)")

    if docs:
        result = await db.master_notes.insert_many(docs)
        print(f"\nTotal: {len(result.inserted_ids)} subjects seeded into '{DATABASE_NAME}.master_notes'")
    else:
        print("No files found.")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
