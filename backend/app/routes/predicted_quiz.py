import json
import os
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/predicted-quiz", tags=["Predicted Quiz"])

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Map of set_id -> filename
SET_FILES = {
    "set_1_comprehensive": "neet_ug_predicted_quiz.json",
    "set_2_high_probability": "neet_ug_predicted_set2.json",
    "set_3_tricky_advanced": "neet_ug_predicted_set3.json",
    "set_4_dark_horse": "neet_ug_predicted_set4.json",
}

_cache = {}


def _load_set(set_id: str):
    if set_id not in SET_FILES:
        raise HTTPException(status_code=404, detail=f"Set '{set_id}' not found")
    if set_id not in _cache:
        path = os.path.join(DATA_DIR, SET_FILES[set_id])
        with open(path, "r", encoding="utf-8") as f:
            _cache[set_id] = json.load(f)
    return _cache[set_id]


@router.get("/sets")
async def list_sets():
    """Return list of all available predicted quiz sets with metadata."""
    sets = []
    for set_id, filename in SET_FILES.items():
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            data = _load_set(set_id)
            sets.append({
                "set_id": set_id,
                "title": data["title"],
                "description": data["description"],
                "total_questions": len(data["questions"]),
                "exam_pattern": data["exam_pattern"],
            })
    return sets


@router.get("/info")
async def get_quiz_info(set_id: str = Query("set_1_comprehensive", description="Quiz set ID")):
    """Return quiz metadata and analysis summary."""
    data = _load_set(set_id)
    result = {
        "title": data["title"],
        "description": data["description"],
        "exam_pattern": data["exam_pattern"],
        "total_questions": len(data["questions"]),
    }
    if "analysis_summary" in data:
        result["analysis_summary"] = data["analysis_summary"]
    if "deep_analysis" in data:
        result["deep_analysis"] = data["deep_analysis"]
    return result


@router.get("/questions")
async def get_questions(
    set_id: str = Query("set_1_comprehensive", description="Quiz set ID"),
    subject: Optional[str] = Query(None, description="Filter by subject: Physics, Chemistry, Biology"),
    chapter: Optional[str] = Query(None, description="Filter by chapter"),
    limit: Optional[int] = Query(None, description="Limit number of questions"),
):
    """Return predicted quiz questions, optionally filtered."""
    data = _load_set(set_id)
    questions = data["questions"]

    if subject:
        questions = [q for q in questions if q["subject"].lower() == subject.lower()]
    if chapter:
        questions = [q for q in questions if chapter.lower() in q["chapter"].lower()]
    if limit and limit > 0:
        questions = questions[:limit]

    return [
        {
            "id": q["id"],
            "subject": q["subject"],
            "chapter": q["chapter"],
            "question": q["question"],
            "options": q["options"],
        }
        for q in questions
    ]


class SubmitAnswer(BaseModel):
    question_id: int
    selected: int  # 0-3 index, -1 for unanswered


class QuizSubmission(BaseModel):
    set_id: str = "set_1_comprehensive"
    answers: list[SubmitAnswer]


@router.post("/submit")
async def submit_quiz(submission: QuizSubmission):
    """Submit answers and get score with explanations."""
    data = _load_set(submission.set_id)
    questions_map = {q["id"]: q for q in data["questions"]}

    correct = 0
    incorrect = 0
    unanswered = 0
    total_marks = 0
    details = []

    for ans in submission.answers:
        q = questions_map.get(ans.question_id)
        if not q:
            continue

        if ans.selected == -1:
            unanswered += 1
            status = "unanswered"
            marks = 0
        elif ans.selected == q["correct"]:
            correct += 1
            status = "correct"
            marks = 4
        else:
            incorrect += 1
            status = "incorrect"
            marks = -1

        total_marks += marks
        details.append({
            "question_id": q["id"],
            "status": status,
            "marks": marks,
            "correct_answer": q["correct"],
            "correct_option": q["options"][q["correct"]],
            "explanation": q["explanation"],
        })

    return {
        "total_questions": len(submission.answers),
        "correct": correct,
        "incorrect": incorrect,
        "unanswered": unanswered,
        "total_marks": total_marks,
        "max_marks": len(submission.answers) * 4,
        "percentage": round((total_marks / (len(submission.answers) * 4)) * 100, 1) if submission.answers else 0,
        "details": details,
    }
