from pydantic import BaseModel
from datetime import date
from typing import List

class IngredientBase(BaseModel):
    name: str
    quantity: int
    purchaseDate: date
    expiryDate: date

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True
