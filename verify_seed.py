import asyncio, os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))
from motor.motor_asyncio import AsyncIOMotorClient

async def verify():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client[os.getenv("DATABASE_NAME")]

    # Count documents
    q_count = await db.questions.count_documents({})
    n_count = await db.notes.count_documents({})
    s_count = await db.subjects.count_documents({})
    print(f"Questions: {q_count}")
    print(f"Notes: {n_count}")
    print(f"Subjects: {s_count}")

    # Subject breakdown
    print("\n--- Questions by Subject ---")
    pipeline = [{"$group": {"_id": "$subject", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}]
    async for doc in db.questions.aggregate(pipeline):
        print(f"  {doc['_id']}: {doc['count']}")

    # Source breakdown
    print("\n--- Questions by Source ---")
    pipeline = [{"$group": {"_id": "$source", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}]
    async for doc in db.questions.aggregate(pipeline):
        print(f"  {doc['_id']}: {doc['count']}")

    # Sample question
    print("\n--- Sample Question ---")
    q = await db.questions.find_one({"subject": "Medicine"})
    if q:
        print(f"  Subject: {q['subject']}")
        print(f"  Question: {q['question'][:100]}...")
        print(f"  Options: {q['options']}")
        print(f"  Correct: {q['correct_answer']}")
        print(f"  Source: {q.get('source', 'N/A')}")

    # Subjects table
    print("\n--- NEET PG Subjects ---")
    async for s in db.subjects.find().sort("name"):
        print(f"  {s['name']}: {s['phase']} | Exam: {s['exam_questions']}Q | Available: {s['available_questions']}Q")

    client.close()

asyncio.run(verify())
