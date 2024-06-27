from ..database import models 
from . import schema 
from . import CRUD as crud 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependency.dependencies import get_db 
from ..database import models

router = APIRouter(
    prefix="/fridge/ingredients",
    tags=["ingredients"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schema.Ingredient, status_code=201)
def add_ingredient(ingredient: schema.IngredientCreate, db: Session = Depends(get_db)):
    return crud.create_ingredient(db=db, ingredient=ingredient)

@router.get("/", response_model=List[schema.Ingredient])
def read_ingredients(name: str = None, purchaseDate: str = None, expiryDate: str = None, db: Session = Depends(get_db)):
    ingredients = crud.get_ingredients(db=db, name=name, purchaseDate=purchaseDate, expiryDate=expiryDate)
    return ingredients

@router.put("/{ingredient_id}", response_model=schema.Ingredient)
def update_ingredient(ingredient_id: int, ingredient: schema.IngredientUpdate, db: Session = Depends(get_db)):
    db_ingredient = crud.update_ingredient(db=db, ingredient_id=ingredient_id, ingredient=ingredient)
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient

@router.delete("/{ingredient_id}", status_code=204)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    db_ingredient = crud.get_ingredient(db, ingredient_id=ingredient_id)
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    crud.delete_ingredient(db=db, ingredient_id=ingredient_id)
    return {"message": "Ingredient deleted successfully"}
