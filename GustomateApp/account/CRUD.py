from sqlalchemy.orm import Session
from ..database.models import Users, Admins
from .schema import UserCreate
from passlib.context import CryptContext
from datetime import datetime
from ..dependency.dependencies import get_password_hash

def create_user(db: Session, user: UserCreate) -> Users:
    hashed_password = get_password_hash(user.password)   # 실제 애플리케이션에서는 비밀번호 해싱 적용 필요
    db_user = Users(
        username=user.username,
        useremail=user.useremail,
        password=hashed_password,
        profile_image=user.profile_image,
        location=user.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> Users:
    return db.query(Users).filter(Users.useremail == email).first()

def get_user(db: Session, user_id: int) -> Users:
    return db.query(Users).filter(Users.user_id == user_id).first()

def delete_user(db: Session, email: str) -> None:
    db.query(Users).filter(Users.useremail == email).delete()
    db.commit()


def create_admin(db: Session, admin: Admins) -> Admins:
    hashed_password = get_password_hash(admin.adminpassword)  # 비밀번호 해싱 적용
    db_admin = Admins(
        adminname=admin.adminname,
        adminemail=admin.adminemail,
        adminpassword=hashed_password
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_admin_by_email(db: Session, email: str) -> Admins:
    return db.query(Admins).filter(Admins.adminemail == email).first()

def delete_admin(db: Session, email: str) -> None:
    db.query(Admins).filter(Admins.adminemail == email).delete()
    db.commit()

async def logout_user(db, token_jti: str, token_exp: datetime):
    await db["token_blacklist"].insert_one({"jti": token_jti, "exp": token_exp})

async def is_token_blacklisted(db, token_jti: str):
    blacklisted_token = await db["token_blacklist"].find_one({"jti": token_jti})
    return blacklisted_token is not None