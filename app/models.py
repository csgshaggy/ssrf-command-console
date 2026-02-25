from pydantic import BaseModel


# -----------------------------
# Authentication Models
# -----------------------------
class UserLogin(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    sub: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -----------------------------
# User Model (used in dependencies)
# -----------------------------
class User(BaseModel):
    username: str
    role: str = "viewer"
