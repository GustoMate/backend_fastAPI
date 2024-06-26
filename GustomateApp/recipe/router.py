from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import Recipe
from .CRUD import get_recipes, get_recipe_review
from ..dependency.dependencies import get_db 
from ..database import models

router = APIRouter()

# 레시피 목록
@router.get("/recipes", response_model=List[Recipe])
async def get_recipe_list(skip: int = 0, limit: int = 6, db: Session = Depends(get_db)):
    recipes = get_recipes(db, skip=skip, limit=limit)
    return recipes

@router.get("/recipes/{recipe_id}", response_model=List[Recipe])
async def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    recipe_reviews = get_recipe_review(db, recipe_id)
    return recipe_reviews