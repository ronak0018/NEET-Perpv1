from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime, timezone
from app.database import get_db
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter(prefix="/api/exam", tags=["Exam"])

MARKS_CORRECT = 4
MARKS_INCORRECT = -1
MARKS_UNANSWERED = 0


class ExamAnswer(BaseModel):
    question_id: str
    selected_answer: int | None = Field(default=None)  # None = unanswered


class ExamSubmission(BaseModel):
    exam_id: str
    answers: list[ExamAnswer]
    time_taken_seconds: int


class ExamStartRequest(BaseModel):
    paper_set_id: str  # e.g. "full_mock", "subject_Anatomy", "source_NEET PG 2024 PYQs"


def question_helper(q) -> dict:
    return {
        "id": str(q["_id"]),
        "subject": q["subject"],
        "topic": q["topic"],
        "question": q["question"],
        "options": q["options"],
        "correct_answer": q["correct_answer"],
        "explanation": q.get("explanation", ""),
        "difficulty": q.get("difficulty", "medium"),
    }


@router.get("/paper-sets")
async def get_paper_sets():
    """Return all available exam paper sets the user can choose from."""
    db = get_db()

    paper_sets = []

    # 1. Full Mock Exam (200 random questions)
    paper_sets.append({
        "id": "full_mock",
        "name": "Full Mock Exam",
        "description": "200 random questions from all subjects – simulates real NEET PG",
        "total_questions": 200,
        "duration_minutes": 210,
        "category": "mock",
        "icon": "🏥",
    })

    # 2. Quick Mock (50 random questions)
    paper_sets.append({
        "id": "quick_mock",
        "name": "Quick Mock Test",
        "description": "50 random questions – quick practice session",
        "total_questions": 50,
        "duration_minutes": 60,
        "category": "mock",
        "icon": "⚡",
    })

    # 3. Subject-wise tests
    subjects = await db.questions.distinct("subject")
    for subject in sorted(subjects):
        count = await db.questions.count_documents({"subject": subject})
        paper_sets.append({
            "id": f"subject_{subject}",
            "name": f"{subject}",
            "description": f"{count} questions available – 50 random per test",
            "total_questions": min(50, count),
            "duration_minutes": 60,
            "category": "subject",
            "icon": "📚",
        })

    # 4. Source-based papers (PYQs, recall papers)
    sources = await db.questions.distinct("source")
    for source in sources:
        if source is None:
            continue
        count = await db.questions.count_documents({"source": source})
        paper_sets.append({
            "id": f"source_{source}",
            "name": source,
            "description": f"{count} questions from {source}",
            "total_questions": count,
            "duration_minutes": max(30, count * 2),
            "category": "pyq",
            "icon": "📝",
        })

    return {"paper_sets": paper_sets}


@router.post("/start")
async def start_exam(request: Optional[ExamStartRequest] = None):
    """Generate a new exam based on the selected paper set."""
    db = get_db()

    # Determine filter and config based on paper_set_id
    paper_set_id = request.paper_set_id if request else "full_mock"

    if paper_set_id == "full_mock":
        total_questions = 200
        duration_seconds = 210 * 60
        pipeline = [{"$sample": {"size": total_questions}}]
    elif paper_set_id == "quick_mock":
        total_questions = 50
        duration_seconds = 60 * 60
        pipeline = [{"$sample": {"size": total_questions}}]
    elif paper_set_id.startswith("subject_"):
        subject = paper_set_id[len("subject_"):]
        total_questions = 50
        duration_seconds = 60 * 60
        pipeline = [{"$match": {"subject": subject}}, {"$sample": {"size": total_questions}}]
    elif paper_set_id.startswith("source_"):
        source = paper_set_id[len("source_"):]
        # For source-based, get ALL matching questions (it's a specific paper)
        total_questions = await db.questions.count_documents({"source": source})
        duration_seconds = max(30 * 60, total_questions * 2 * 60)
        pipeline = [{"$match": {"source": source}}]
    else:
        raise HTTPException(status_code=400, detail="Invalid paper set ID")

    questions = []
    async for q in db.questions.aggregate(pipeline):
        questions.append(question_helper(q))

    if len(questions) == 0:
        raise HTTPException(status_code=400, detail="No questions found for this paper set.")

    max_marks = len(questions) * MARKS_CORRECT

    # Save exam set to DB
    exam_doc = {
        "question_ids": [q["id"] for q in questions],
        "paper_set_id": paper_set_id,
        "total_questions": len(questions),
        "duration_seconds": duration_seconds,
        "created_at": datetime.now(timezone.utc),
        "status": "in_progress",
    }
    result = await db.exams.insert_one(exam_doc)

    return {
        "exam_id": str(result.inserted_id),
        "questions": questions,
        "total_questions": len(questions),
        "duration_seconds": duration_seconds,
        "max_marks": max_marks,
    }


@router.post("/submit")
async def submit_exam(submission: ExamSubmission):
    """Submit exam and calculate NEET PG scoring."""
    db = get_db()

    # Validate exam exists
    if not ObjectId.is_valid(submission.exam_id):
        raise HTTPException(status_code=400, detail="Invalid exam ID")

    exam = await db.exams.find_one({"_id": ObjectId(submission.exam_id)})
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    # Calculate score
    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    results = []

    for ans in submission.answers:
        if not ObjectId.is_valid(ans.question_id):
            continue
        question = await db.questions.find_one({"_id": ObjectId(ans.question_id)})
        if not question:
            continue

        if ans.selected_answer is None or ans.selected_answer == -1:
            unanswered_count += 1
            status = "unanswered"
            is_correct = False
        elif question["correct_answer"] == ans.selected_answer:
            correct_count += 1
            status = "correct"
            is_correct = True
        else:
            incorrect_count += 1
            status = "incorrect"
            is_correct = False

        results.append({
            "question_id": ans.question_id,
            "question": question["question"],
            "options": question["options"],
            "selected_answer": ans.selected_answer,
            "correct_answer": question["correct_answer"],
            "explanation": question.get("explanation", ""),
            "subject": question["subject"],
            "topic": question["topic"],
            "status": status,
            "is_correct": is_correct,
        })

    raw_score = (MARKS_CORRECT * correct_count) + (MARKS_INCORRECT * incorrect_count) + (MARKS_UNANSWERED * unanswered_count)
    max_marks = exam["total_questions"] * MARKS_CORRECT
    percentage = round((raw_score / max_marks) * 100, 2) if max_marks > 0 else 0

    # Update exam status
    exam_result = {
        "exam_id": submission.exam_id,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "unanswered_count": unanswered_count,
        "raw_score": raw_score,
        "max_marks": max_marks,
        "percentage": percentage,
        "time_taken_seconds": submission.time_taken_seconds,
        "submitted_at": datetime.now(timezone.utc),
    }

    await db.exams.update_one(
        {"_id": ObjectId(submission.exam_id)},
        {"$set": {"status": "completed", "result": exam_result}}
    )

    return {
        **exam_result,
        "total_questions": exam["total_questions"],
        "marks_correct": MARKS_CORRECT,
        "marks_incorrect": MARKS_INCORRECT,
        "results": results,
    }


@router.get("/history")
async def get_exam_history():
    """Get list of past exam attempts."""
    db = get_db()
    exams = []
    cursor = db.exams.find({"status": "completed"}).sort("result.submitted_at", -1).limit(20)
    async for exam in cursor:
        exams.append({
            "exam_id": str(exam["_id"]),
            "created_at": exam["created_at"].isoformat(),
            "result": exam.get("result"),
        })
    return exams
