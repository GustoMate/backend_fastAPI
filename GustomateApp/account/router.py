from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schema import UserCreate, User, Admin
from .CRUD import create_user, get_user_by_email, get_admin_by_email, create_admin
from ..dependency.dependencies import get_db, authenticate_accounts
from ..database import models
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.security import OAuth2PasswordRequestForm
from ..dependency.dependencies import oauth2_scheme, create_access_token, admin_oauth2_scheme

router = APIRouter()

# 회원가입
@router.post("/signup", response_model=User)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 데이터베이스에서 이메일 중복 확인
    existing_user = get_user_by_email(db, email=user.useremail)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 새 사용자를 데이터베이스에 추가
    new_user = create_user(db=db, user=user)
    return new_user

# 관리자 회원가입
@router.post("/admin/signup", response_model=Admin)
async def admin_signup(admin: Admin, db: Session = Depends(get_db)):
    # 데이터베이스에서 이메일 중복 확인
    existing_admin = get_admin_by_email(db, email=admin.adminemail)
    if existing_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 새 관리자를 데이터베이스에 추가
    new_admin = create_admin(db=db, admin=admin)
    return new_admin

# 로그인
@router.post("/login")
async def login_for_access_token(request: Request, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_accounts(db, email=form_data.username, password=form_data.password, is_admin=False)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.useremail, "scope": "user"})
    request.session['token'] = access_token
    request.session['user_email'] = user.useremail
    return {
        "message": "User logged in successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.useremail
    }

# 관리자 로그인
@router.post("/admin/login")
async def admin_login_for_access_token(request: Request, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    admin = await authenticate_accounts(db, email=form_data.username, password=form_data.password, is_admin=True)
    if not admin:
        raise HTTPException(status_code=401, detail="Incorrect admin email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": admin.adminemail, "scope": "admin"})
    request.session['token'] = access_token
    request.session['admin_email'] = admin.adminemail
    return {
        "message": "Admin logged in successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "email": admin.adminemail
    }