from ninja import Schema
from typing import Optional
from pydantic import BaseModel, EmailStr


class AuthSchema(Schema):
    password: str
    email: EmailStr


class Message(Schema):
    message: str


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"


class OneInputToken(BaseModel):
    token: str


class Error(BaseModel):
    code: int
    message: str


class BoolSignal(BaseModel):
    bool: bool
