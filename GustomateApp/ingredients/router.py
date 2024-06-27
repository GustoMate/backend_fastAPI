from ..database import models 
from . import schema as schemas
from .CRUD import get_ingredient, get_ingredients, create_ingredient, update_ingredient, delete_ingredient 
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from ..dependency.dependencies import get_db 
from ..database import models
from ..dependency.dependencies import get_current_user
from ..dependency.dependencies import get_token_from_session



router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=schemas.Ingredient, status_code=201)
async def add_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    return create_ingredient(db=db, ingredient=ingredient, user_id=current_user.user_id)

@router.get("", response_model=List[schemas.Ingredient])
async def read_ingredients(db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    ingredients = get_ingredients(db=db, user_id=current_user.user_id)
    return ingredients

@router.put("/{ingredient_id}", response_model=schemas.Ingredient)
async def modify_ingredient(ingredient_id: int, ingredient: schemas.IngredientUpdate, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    db_ingredient = update_ingredient(db=db, ingredient_id=ingredient_id, ingredient=ingredient)
    if db_ingredient is None or db_ingredient.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient

@router.delete("/{ingredient_id}", status_code=204)
async def remove_ingredient(ingredient_id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    db_ingredient = get_ingredient(db, ingredient_id=ingredient_id)
    if db_ingredient is None or db_ingredient.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    delete_ingredient(db=db, ingredient_id=ingredient_id)
    return {"message": "Ingredient deleted successfully"}