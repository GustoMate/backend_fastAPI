from sqlalchemy.orm import Session
from ..database.models import Recipes, Recipe_Reviews

def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Recipes).offset(skip).limit(limit).all()

def get_recipe_review(db: Session, recipe_id: int):
    return db.query(Recipe_Reviews).filter(Recipe_Reviews.recipe_id == recipe_id).all()

def search_recipes(db: Session, query: str):
    return db.query(Recipes).filter(Recipes.recipe_name.ilike(f"{query}")).all()