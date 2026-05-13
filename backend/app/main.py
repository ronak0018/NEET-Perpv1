from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_db, close_db
from app.routes.questions import router as questions_router
from app.routes.notes import router as notes_router
from app.routes.exam import router as exam_router

app = FastAPI(title="NEET PG Prep", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await connect_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db()


@app.get("/")
async def root():
    return {"message": "NEET PG Prep API"}


app.include_router(questions_router)
app.include_router(notes_router)
app.include_router(exam_router)
