from pydantic import BaseModel, EmailStr
from datetime import datetime

# Recipe: Recipe 정보
class Recipe(BaseModel):
    recipe_id: int
    recipe_name: str
    image: str
    difficulty: int
    steps: str
    cuisine_id: int
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
