from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from datetime import datetime
from app.database import get_db
from app.models import QuestionCreate, QuestionResponse, QuizSubmission, QuizResult

router = APIRouter(prefix="/api/questions", tags=["Questions"])


def question_helper(q) -> dict:
    return {
        "id": str(q["_id"]),
        "subject": q["subject"],
        "topic": q["topic"],
        "question": q["question"],
        "options": q["options"],
        "correct_answer": q["correct_answer"],
        "explanation": q["explanation"],
        "difficulty": q["difficulty"],
        "created_at": q["created_at"],
    }


@router.post("/", response_model=QuestionResponse, status_code=201)
async def create_question(question: QuestionCreate):
    db = get_db()
    doc = question.model_dump()
    doc["created_at"] = datetime.utcnow()
    result = await db.questions.insert_one(doc)
    created = await db.questions.find_one({"_id": result.inserted_id})
    return question_helper(created)


@router.get("/", response_model=list[QuestionResponse])
async def get_questions(
    subject: str | None = None,
    topic: str | None = None,
    difficulty: str | None = None,
    limit: int = Query(default=20, le=100),
    skip: int = 0,
):
    db = get_db()
    query = {}
    if subject:
        query["subject"] = subject
    if topic:
        query["topic"] = topic
    if difficulty:
        query["difficulty"] = difficulty

    cursor = db.questions.find(query).skip(skip).limit(limit)
    questions = []
    async for q in cursor:
        questions.append(question_helper(q))
    return questions


@router.get("/subjects")
async def get_subjects():
    db = get_db()
    subjects = await db.questions.distinct("subject")
    return subjects


@router.get("/topics/{subject}")
async def get_topics(subject: str):
    db = get_db()
    topics = await db.questions.distinct("topic", {"subject": subject})
    return topics


@router.get("/quiz")
async def get_quiz(
    subject: str | None = None,
    topic: str | None = None,
    difficulty: str | None = None,
    count: int = Query(default=10, le=50),
):
    db = get_db()
    pipeline = []
    match_stage = {}
    if subject:
        match_stage["subject"] = subject
    if topic:
        match_stage["topic"] = topic
    if difficulty:
        match_stage["difficulty"] = difficulty
    if match_stage:
        pipeline.append({"$match": match_stage})
    pipeline.append({"$sample": {"size": count}})

    questions = []
    async for q in db.questions.aggregate(pipeline):
        questions.append(question_helper(q))
    return questions


@router.post("/submit-quiz", response_model=QuizResult)
async def submit_quiz(submissions: list[QuizSubmission]):
    db = get_db()
    correct = 0
    results = []

    for sub in submissions:
        if not ObjectId.is_valid(sub.question_id):
            raise HTTPException(status_code=400, detail=f"Invalid question ID: {sub.question_id}")
        question = await db.questions.find_one({"_id": ObjectId(sub.question_id)})
        if not question:
            raise HTTPException(status_code=404, detail=f"Question not found: {sub.question_id}")

        is_correct = question["correct_answer"] == sub.selected_answer
        if is_correct:
            correct += 1

        results.append({
            "question_id": sub.question_id,
            "question": question["question"],
            "selected_answer": sub.selected_answer,
            "correct_answer": question["correct_answer"],
            "is_correct": is_correct,
            "explanation": question["explanation"],
        })

    total = len(submissions)
    return QuizResult(
        total_questions=total,
        correct_answers=correct,
        wrong_answers=total - correct,
        score_percentage=round((correct / total) * 100, 2) if total > 0 else 0,
        results=results,
    )


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: str):
    if not ObjectId.is_valid(question_id):
        raise HTTPException(status_code=400, detail="Invalid question ID")
    db = get_db()
    question = await db.questions.find_one({"_id": ObjectId(question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question_helper(question)


@router.delete("/{question_id}", status_code=204)
async def delete_question(question_id: str):
    if not ObjectId.is_valid(question_id):
        raise HTTPException(status_code=400, detail="Invalid question ID")
    db = get_db()
    result = await db.questions.delete_one({"_id": ObjectId(question_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")
