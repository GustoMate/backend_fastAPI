from sqlalchemy.orm import Session
from ..database.models import Users
from .schema import UserCreate

def create_user(db: Session, user: UserCreate) -> Users:
    hashed_password = user.password  # 실제 애플리케이션에서는 비밀번호 해싱 적용 필요
    db_user = Users(
        nickname=user.nickname,
        email=user.email,
        password=hashed_password,
        profile_image=user.profile_image,
        location=user.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Users:
    return db.query(Users).filter(Users.user_id == user_id).first()

