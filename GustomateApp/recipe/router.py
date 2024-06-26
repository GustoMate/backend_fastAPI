from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import Recipe, RecipeReviews
from .CRUD import get_recipes, get_recipe_review, search_recipes
from ..dependency.dependencies import get_db 
from ..database import models

router = APIRouter()

# 레시피 목록
@router.get("/recipes", response_model=List[Recipe])
async def get_recipe_list(skip: int = 0, limit: int = 6, db: Session = Depends(get_db)):
    recipes = get_recipes(db, skip=skip, limit=limit)
    return recipes


# 레시피 검색
@router.get("/recipes/search", response_model=List[Recipe])
async def search_recipe(query: str, db: Session = Depends(get_db)):
    recipes = search_recipes(db, query)
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found for the search query")
    return recipes


# 레시피 상세 정보 및 리뷰
@router.get("/recipes/{recipe_id}", response_model=List[RecipeReviews])
async def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    recipe_reviews = get_recipe_review(db, recipe_id)
    return recipe_reviews