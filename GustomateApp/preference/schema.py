from pydantic import BaseModel
from typing import Optional

class UserPreferenceBase(BaseModel):
    spiciness_preference: int
    cooking_skill: int
    is_on_diet: bool
    allergies: Optional[str] = None

class UserPreferenceCreate(UserPreferenceBase):
    user_id: int

class UserPreferenceUpdate(UserPreferenceBase):
    pass

class UserPreference(UserPreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
