from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class QuestionCreate(BaseModel):
    subject: str
    topic: str
    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: int = Field(..., ge=0, le=3)
    explanation: str
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")


class QuestionResponse(QuestionCreate):
    id: str
    created_at: datetime


class NoteCreate(BaseModel):
    subject: str
    topic: str
    title: str
    content: str


class NoteUpdate(BaseModel):
    subject: Optional[str] = None
    topic: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None


class NoteResponse(NoteCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class QuizSubmission(BaseModel):
    question_id: str
    selected_answer: int = Field(..., ge=0, le=3)


class QuizResult(BaseModel):
    total_questions: int
    correct_answers: int
    wrong_answers: int
    score_percentage: float
    results: list[dict]
