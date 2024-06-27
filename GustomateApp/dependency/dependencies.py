from sqlalchemy.orm import Session
from ..database.database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from uuid import uuid4
from ..account.schema import TokenData
from ..database.models import Users, Admins, TokenBlacklist
from fastapi import HTTPException, Depends
from starlette.requests import Request
from jose import jwt, JWTError
from ..database.models import TokenBlacklist



# JWT 토큰 설정
#openssl rand -hex 32로 생성, 프로덕션 환경으로 이동하기 전에 secret_key 바꿀 예정, 그땐 git에 업로드 x
SECRET_KEY = "dcd5b09a1d67d762d34cef0fc0be7017c6cd05834b3be25cc80491045e0c205f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/admin/login")

# 데이터베이스 세션을 가져오는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 세션에서 토큰을 가져오는 함수 추가
async def get_token_from_session(request: Request):
    return request.session.get('token')

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "jti": str(uuid4())})  # JTI added
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_accounts(db: Session, email: str, password: str, is_admin: bool):
    if not is_admin:
        account = db.query(Users).filter(Users.useremail == email).first()
    else:
        account = db.query(Admins).filter(Admins.adminemail == email).first()
    if account and verify_password(password, account.password if not is_admin else account.adminpassword):
        return account
    return None

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = decode_access_token(token)
        if payload.get("jti") is None or await is_token_blacklisted(db, payload["jti"]):
            raise credentials_exception
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(Users).filter(Users.useremail == email).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(db: Session = Depends(get_db), token: str = Depends(admin_oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = decode_access_token(token)
        if payload.get("jti") is None or await is_token_blacklisted(db, payload["jti"]):
            raise credentials_exception
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    admin = db.query(Admins).filter(Admins.adminemail == email).first()
    if admin is None:
        raise credentials_exception
    return admin

async def is_token_blacklisted(db: Session, token_jti: str):
    blacklisted_token = db.query(TokenBlacklist).filter(TokenBlacklist.jti == token_jti).first()
    return blacklisted_token is not None