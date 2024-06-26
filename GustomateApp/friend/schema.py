from pydantic import BaseModel, EmailStr
from datetime import datetime

class Friends(BaseModel):
    user_id: int
    friend_id: int
    created_at: datetime
    updated_at: datetime

class FriendDetail(BaseModel):
    friend_id: int
    friend_name: str
    friend_email: str
    friend_location: str
    created_at: datetime
    updated_at: datetime
