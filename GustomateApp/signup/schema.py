from pydantic import BaseModel, EmailStr
from datetime import datetime

# UserCreate: User 생성 시 필요한 정보
class UserCreate(BaseModel):
    nickname: str
    username: EmailStr
    password: str
    profile_image: str
    location: str

# User: User 정보
class User(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    profile_image: str
    location: str
    created_at: datetime

    class Config:
        from_attributes = True

