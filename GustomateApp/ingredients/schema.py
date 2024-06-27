from pydantic import BaseModel
from datetime import date


class IngredientBase(BaseModel):
    name: str
    quantity: int
    purchaseDate: date
    expiryDate: date

class IngredientCreate(IngredientBase):
    user_id: int

class IngredientUpdate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
