"""Debug script to reproduce the /api/notes/ 500 error"""
import asyncio
import traceback
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / "backend" / ".env")
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "neetpg")


class NoteCreate(BaseModel):
    subject: str
    topic: str
    title: str
    content: str

class NoteResponse(NoteCreate):
    id: str
    created_at: datetime
    updated_at: datetime


def note_helper(n) -> dict:
    return {
        "id": str(n["_id"]),
        "subject": n["subject"],
        "topic": n["topic"],
        "title": n["title"],
        "content": n["content"],
        "created_at": n["created_at"],
        "updated_at": n["updated_at"],
    }


async def main():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        # Reproduce exactly what the route does
        cursor = db.notes.find({}).sort("updated_at", -1).skip(0).limit(20)
        notes = []
        async for n in cursor:
            try:
                helper_result = note_helper(n)
                # Try Pydantic validation too
                validated = NoteResponse(**helper_result)
                notes.append(helper_result)
            except Exception as e:
                print(f"ERROR on note: {n.get('title', 'unknown')}")
                print(f"  Keys: {list(n.keys())}")
                print(f"  Exception: {type(e).__name__}: {e}")
                print(f"  created_at type: {type(n.get('created_at'))}, value: {n.get('created_at')}")
                print(f"  updated_at type: {type(n.get('updated_at'))}, value: {n.get('updated_at')}")
                traceback.print_exc()
                print()
        
        print(f"Successfully processed {len(notes)} notes")
        
    except Exception as e:
        print(f"TOP-LEVEL ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()
    finally:
        client.close()


asyncio.run(main())
