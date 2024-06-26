from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime, date
from pydantic import BaseModel

# 데이터베이스 테이블 모델
class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key= True, index = True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    profile_image = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)

class User_Preferences(Base):
    __tablename__ = "user_preferences"

    user_preference_id = Column(Integer, primary_key= True, index = True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    spiciness_preference = Column(Integer)
    cooking_skill = Column(String)
    fridge_public = Column(Boolean)
    notification_enabled = Column(Boolean)
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)
    
class Chats(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key= True, index = True)
    user1_id = Column(Integer, ForeignKey("users.user_id"))
    user2_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)

class Recipe(Base):
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

