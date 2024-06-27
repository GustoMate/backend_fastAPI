from pydantic import BaseModel
from datetime import date

class IngredientBase(BaseModel):
    name: str
    quantity: int
    expiryDate: date
    description: str

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
