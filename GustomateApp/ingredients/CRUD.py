from sqlalchemy.orm import Session
from . import schema as schemas
from ..database import models


def get_ingredient(db: Session, ingredient_id: int):
    return db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()

def get_ingredients(db: Session, user_id: int):
    return db.query(models.Ingredient).filter(models.Ingredient.user_id == user_id).all()

def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
    db_ingredient = models.Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def update_ingredient(db: Session, ingredient_id: int, ingredient: schemas.IngredientUpdate):
    db_ingredient = get_ingredient(db, ingredient_id)
    if db_ingredient:
        for key, value in ingredient.dict().items():
            setattr(db_ingredient, key, value)
        db.commit()
        db.refresh(db_ingredient)
    return db_ingredient

def delete_ingredient(db: Session, ingredient_id: int):
    db_ingredient = get_ingredient(db, ingredient_id)
    if db_ingredient:
        db.delete(db_ingredient)
        db.commit()
    return db_ingredient