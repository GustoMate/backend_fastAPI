from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schema import UserCreate, User
from .CRUD import create_user  
from ..dependency.dependencies import get_db 
from ..database import models

router = APIRouter()

# 회원가입
@router.post("/signup", response_model=User)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 데이터베이스에서 이메일 중복 확인
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 새 사용자를 데이터베이스에 추가
    new_user = create_user(db=db, user=user)
    return new_user
