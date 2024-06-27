from pydantic import BaseModel, Field
from typing import List

class UserPreferenceBase(BaseModel):
    spiciness_preference: float
    cooking_skill: float
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
        from_attributes = True  # Pydantic V2에서는 'orm_mode' 대신 'from_attributes'를 사용합니다.