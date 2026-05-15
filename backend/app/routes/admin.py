from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# Admin credentials (change these)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "neetpg2026"


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def admin_login(creds: LoginRequest):
    if creds.username == ADMIN_USERNAME and creds.password == ADMIN_PASSWORD:
        return {"success": True, "message": "Authenticated"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/activity")
async def get_activity(username: str = "", password: str = ""):
    """Return recent user activity. Requires admin credentials as query params."""
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    db = get_db()
    cursor = db.user_activity.find().sort("timestamp", -1).limit(100)
    activities = []
    async for doc in cursor:
        activities.append({
            "id": str(doc["_id"]),
            "action": doc.get("action", ""),
            "detail": doc.get("detail", ""),
            "ip": doc.get("ip", ""),
            "user_agent": doc.get("user_agent", ""),
            "timestamp": doc.get("timestamp", ""),
        })
    return activities


@router.post("/track")
async def track_activity(request: Request):
    """Log user activity (called from frontend)."""
    db = get_db()
    body = await request.json()
    doc = {
        "action": body.get("action", "page_view"),
        "detail": body.get("detail", ""),
        "username": body.get("username", ""),
        "ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "timestamp": datetime.utcnow().isoformat(),
    }
    await db.user_activity.insert_one(doc)
    return {"status": "tracked"}


@router.get("/users")
async def get_users(username: str = "", password: str = ""):
    """Return app user last-login info. Requires admin credentials."""
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    db = get_db()
    cursor = db.app_users.find()
    users = []
    async for doc in cursor:
        users.append({
            "username": doc.get("username", ""),
            "last_login": doc.get("last_login", ""),
            "ip": doc.get("ip", ""),
            "user_agent": doc.get("user_agent", ""),
        })
    return users
