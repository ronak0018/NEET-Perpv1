from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db

router = APIRouter(prefix="/api/auth", tags=["Auth"])

# App users
USERS = {
    "shreya": "shreya@123",
    "demo": "demo@123",
}


class UserLoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def user_login(creds: UserLoginRequest, request: Request):
    if creds.username in USERS and USERS[creds.username] == creds.password:
        # Try to record last login, but don't fail if DB is unavailable
        try:
            db = get_db()
            await db.app_users.update_one(
                {"username": creds.username},
                {
                    "$set": {
                        "last_login": datetime.utcnow().isoformat(),
                        "ip": request.client.host if request.client else "unknown",
                        "user_agent": request.headers.get("user-agent", "unknown"),
                    }
                },
                upsert=True,
            )
        except Exception:
            pass
        return {"success": True, "username": creds.username}
    raise HTTPException(status_code=401, detail="Invalid username or password")
