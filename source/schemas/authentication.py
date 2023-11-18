from pydantic import BaseModel
from typing import Optional

class UserOut(BaseModel):
    email: str
    name: str
    id: int

class UserAuth(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
