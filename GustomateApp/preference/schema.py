from pydantic import BaseModel
from typing import List

class UserPreferenceBase(BaseModel):
    spiciness_preference: int
    cooking_skill: int
    is_on_diet: bool
    has_allergies: bool  # 알러지 여부
    allergies: List[str] = []  # 알러지 목록

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceUpdate(UserPreferenceBase):
    pass

class UserPreference(UserPreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
