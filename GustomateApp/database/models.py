from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from datetime import datetime, date
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative
import json


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True, nullable=False)
    exp = Column(DateTime, nullable=False)

# 데이터베이스 테이블 모델


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    expiryDate = Column(Date, nullable=False)
    description = Column(String, nullable=False)



@as_declarative()
class Base:
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, index=True)
    spiciness_preference = Column(Integer)
    cooking_skill = Column(Integer)
    is_on_diet = Column(Boolean)
    has_allergies = Column(Boolean)
    allergies = Column(Text)  # JSON 형태로 저장

    def __init__(self, **kwargs):
        if 'allergies' in kwargs:
            kwargs['allergies'] = json.dumps(kwargs['allergies'])
        super().__init__(**kwargs)

    def as_dict(self):
        result = super().as_dict()
        result['allergies'] = json.loads(result['allergies'])
        return result



@as_declarative()
class Base:
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, index=True)
    spiciness_preference = Column(Integer)
    cooking_skill = Column(Integer)
    is_on_diet = Column(Boolean)
    has_allergies = Column(Boolean)
    allergies = Column(Text)  # JSON 형태로 저장

    def __init__(self, **kwargs):
        if 'allergies' in kwargs:
            kwargs['allergies'] = json.dumps(kwargs['allergies'])
        super().__init__(**kwargs)

    def as_dict(self):
        result = super().as_dict()
        result['allergies'] = json.loads(result['allergies'])
        return result


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

    recipe_id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String)
    image = Column(String)
    method_classification = Column(String)  # 수정된 부분
    country_classification = Column(String)
    theme_classification = Column(String)
    difficulty_classification = Column(String)
    calorie = Column(Integer)
    view = Column(Integer)
    quantity = Column(Integer)
    main_ingredients = Column(String)
    sub_ingredients = Column(String)
    seasonings = Column(String)
    recipe = Column(String)
    cooking_time = Column(Integer)
    spiciness = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

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

class Market(Base):
    __tablename__ = "market"

    market_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    market_image = Column(String)
    market_description = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)

