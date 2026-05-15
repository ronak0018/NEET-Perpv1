from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_db, close_db
from app.routes.questions import router as questions_router
from app.routes.notes import router as notes_router
from app.routes.exam import router as exam_router
from app.routes.detailed_study import router as detailed_study_router
from app.routes.master_notes import router as master_notes_router
from app.routes.admin import router as admin_router
from app.routes.auth import router as auth_router

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


@app.get("/api/health")
async def health():
    return {"status": "alive"}


app.include_router(questions_router)
app.include_router(notes_router)
app.include_router(exam_router)
app.include_router(detailed_study_router)
app.include_router(master_notes_router)
app.include_router(admin_router)
app.include_router(auth_router)
