from pydantic import BaseModel, EmailStr
from datetime import datetime

# Recipe: Recipe 정보
class Recipe(BaseModel):
    recipe_id: int
    recipe_name: str
    image: str
    method_classification: str
    country_classification: str
    theme_classification: str
    difficulty_classification: str
    calorie: int
    view: int
    quantity: int
    main_ingredients: str
    sub_ingredients: str
    seasonings: str
    recipe: str
    cooking_time: int
    spiciness: int
    created_at: datetime
    updated_at: datetime


class RecipeReviews(BaseModel):
    review_id: int
    recipe_id: int
    user_id: int
    review_header: str
    review_text: str
    rating: int
    created_at: datetime
    updated_at: datetime


