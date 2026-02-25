# app/routers/auth.py

from fastapi import APIRouter, HTTPException
import json

from app.core.security import verify_password, create_access_token
from app.config import settings
from app.models import UserLogin

router = APIRouter()


@router.post("/login", summary="Authenticate user and return token")
def login(credentials: UserLogin):
    username = credentials.username
    password = credentials.password

    # Load users.json
    try:
        with open("/app/app/users.json", "r") as f:
            users = json.load(f)
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to load user database")

    if username not in users:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    stored_hash = users[username]["password"]

    if not verify_password(password, stored_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": username})

    return {"access_token": token, "token_type": "bearer"}
