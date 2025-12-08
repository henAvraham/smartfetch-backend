from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl, Field, field_validator
from typing import Optional, List
import re




class UserCreate(BaseModel):
    username: str = Field(..., min_length=1)
    password: str
    @field_validator("password")
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*()_\-+={}\[\]|\\:;\"'<>,.?/~`]", v):
            raise ValueError("Password must contain at least one special character.")

      
        numeric_sequences = [
            "0123", "1234", "2345", "3456",
            "4567", "5678", "6789", "7890",
        ]
        if any(seq in v for seq in numeric_sequences):
            raise ValueError("Password cannot contain sequential numbers like 1234.")

        if re.search(r"(.)\1{3,}", v):
            raise ValueError("Password cannot contain the same character repeated many times in a row.")

        return v


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True




class Token(BaseModel):
    access_token: str
    token_type: str



class SourceCreate(BaseModel):
    url: HttpUrl


class SourceRead(BaseModel):
    id: int
    url: HttpUrl
    created_at: datetime

    class Config:
        orm_mode = True




class DocumentRead(BaseModel):
    id: int
    source_id: int
    url: HttpUrl
    title: Optional[str] = None
    content: str
    created_at: datetime

    class Config:
        orm_mode = True




class AskRequest(BaseModel):
    question: str
    source_id: Optional[int] = None
       
class RetrievedChunk(BaseModel):
    id: str
    score: float
    doc_id: int
    user_id: int
    source_id: int
    title: Optional[str] = None
    content: str
    url: Optional[str] = None


class AskResponse(BaseModel):
    answer: str
    chunks: List[RetrievedChunk]