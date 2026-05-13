"""
Seed NEET PG questions from JSON batch files into MongoDB.
Transforms JSON format (options as {label,text}, correct_answer as text)
to DB format (options as strings, correct_answer as index 0-3).
"""
import json
import os
import glob
import time
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join("backend", ".env"))

MONGO_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DATABASE_NAME", "neetpg")
JSON_DIR = os.path.join("Files", "questions")

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=30000, connectTimeoutMS=30000, socketTimeoutMS=60000)
db = client[DB_NAME]

# Map difficulty values to what the schema expects
DIFFICULTY_MAP = {
    "NEET PG": "hard",
    "neet pg": "hard",
    "easy": "easy",
    "medium": "medium",
    "hard": "hard",
}

files = sorted(glob.glob(os.path.join(JSON_DIR, "NEETPG_QuestionBank_Batch_*_2000.json")))
print(f"Found {len(files)} batch files")

# Get existing batch_ids to skip duplicates
existing_ids = set(db.questions.distinct("batch_id"))
print(f"Already in DB: {len(existing_ids)} batch_ids")

total_inserted = 0
total_skipped = 0

for filepath in files:
    batch_name = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = data.get("questions", [])
    docs = []

    for q in questions:
        # Skip if already inserted
        qid = q.get("id", "")
        if qid in existing_ids:
            total_skipped += 1
            continue

        # Convert options from [{label, text}] to [text]
        option_texts = [opt["text"] for opt in q["options"]]

        # Find correct_answer index
        correct_text = q["correct_answer"]
        correct_idx = None
        for i, opt in enumerate(option_texts):
            if opt == correct_text:
                correct_idx = i
                break

        if correct_idx is None:
            # Try case-insensitive match
            for i, opt in enumerate(option_texts):
                if opt.lower().strip() == correct_text.lower().strip():
                    correct_idx = i
                    break

        if correct_idx is None:
            total_skipped += 1
            continue

        difficulty = DIFFICULTY_MAP.get(q.get("difficulty", "medium"), "medium")

        doc = {
            "subject": q["subject"],
            "topic": q["topic"],
            "question": q["question"],
            "options": option_texts,
            "correct_answer": correct_idx,
            "explanation": q.get("explanation", ""),
            "difficulty": difficulty,
            "batch_id": q.get("id", ""),
            "created_at": datetime.now(timezone.utc),
        }
        docs.append(doc)

    if docs:
        # Insert in small chunks with retry and reconnect
        chunk_size = 25
        inserted = 0
        for i in range(0, len(docs), chunk_size):
            chunk = docs[i:i + chunk_size]
            for attempt in range(3):
                try:
                    result = db.questions.insert_many(chunk, ordered=False)
                    inserted += len(result.inserted_ids)
                    break
                except KeyboardInterrupt:
                    raise
                except BaseException as e:
                    if attempt < 2:
                        time.sleep(3)
                        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=30000, connectTimeoutMS=30000, socketTimeoutMS=120000)
                        db = client[DB_NAME]
                    else:
                        print(f"    FAILED chunk {i//chunk_size+1}: {e}")
            if inserted > 0 and inserted % 500 < chunk_size:
                print(f"    ... {inserted}/{len(docs)} inserted", flush=True)
            time.sleep(0.1)  # Brief pause between chunks
        total_inserted += inserted
        print(f"  {batch_name}: inserted {inserted}, skipped {len(questions) - len(docs)}", flush=True)
    else:
        print(f"  {batch_name}: no valid questions found", flush=True)

print(f"\nDone! Total inserted: {total_inserted}, skipped: {total_skipped}")
print(f"Total questions in DB: {db.questions.count_documents({})}")

client.close()
