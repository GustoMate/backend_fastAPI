from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime, date
from pydantic import BaseModel
from sqlalchemy.orm import relationship

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True, nullable=False)
    exp = Column(DateTime, nullable=False)

# 데이터베이스 테이블 모델
class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key= True, index = True)
    username = Column(String)
    useremail = Column(String)
    password = Column(String)
    profile_image = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)


class Chats(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key= True, index = True)
    user1_id = Column(Integer, ForeignKey("users.user_id"))
    user2_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)

class Recipes(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key= True, index = True)
    recipe_name = Column(String)
    image = Column(String)
    difficulty = Column(Integer)
    steps = Column(String)
    cuisine_id = Column(Integer, ForeignKey("cuisines.cuisine_id"))
    spiciness = Column(Integer)
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)

class Recipe_Reviews(Base):
    __tablename__ = "recipe_reviews"

    review_id = Column(Integer, primary_key= True, index = True)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    review_header = Column(String)
    review_text = Column(String)
    rating = Column(Integer)
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)


class Admins(Base):
    __tablename__ = "admins"

    admin_id = Column(Integer, primary_key= True, index = True)
    adminname = Column(String)
    adminemail = Column(String)
    adminpassword = Column(String)
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)

class Friends(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key= True, index = True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    friend_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    name = Column(String, index=True)
    quantity = Column(Integer)
    purchaseDate = Column(Date)
    expiryDate = Column(Date)

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    spiciness_preference = Column(Integer)
    cooking_skill = Column(Integer)
    is_on_diet = Column(Boolean)
    allergies = Column(String, nullable=True)
