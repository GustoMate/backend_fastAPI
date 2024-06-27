from pydantic import BaseModel
from datetime import date

class UserPreferenceBase(BaseModel):
    spiciness_preference: int
    cooking_skill: int
    is_on_diet: bool
    allergies: str

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceUpdate(UserPreferenceBase):
    pass

class UserPreference(UserPreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
