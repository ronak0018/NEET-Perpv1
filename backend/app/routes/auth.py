from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db

router = APIRouter(prefix="/api/auth", tags=["Auth"])

# App users
USERS = {
    "shreya": "shreya@123",
    "demo": "demo@123",
    "rohit": "sonu@1818",
}


class UserLoginRequest(BaseModel):
    username: str
    password: str


ROLES = {
    "shreya": "full",
    "demo": "full",
    "rohit": "exam_only",
}


@router.post("/login")
async def user_login(creds: UserLoginRequest, request: Request):
    if creds.username in USERS and USERS[creds.username] == creds.password:
        db = get_db()
        # Update last login time
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
        return {"success": True, "username": creds.username, "role": ROLES.get(creds.username, "full")}
    raise HTTPException(status_code=401, detail="Invalid username or password")
