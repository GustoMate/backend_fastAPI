from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional, Dict


# UserCreate: User 생성 시 필요한 정보
class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="사용자의 닉네임")
    useremail: EmailStr = Field(..., description="사용자의 이메일 주소")
    password: str = Field(..., min_length=8, description="사용자의 비밀번호")
    profile_image: str = Field(default=None, description="사용자의 프로필 이미지 URL")
    location: str = Field(..., max_length=100, description="사용자의 위치")

# User: User 정보
class User(BaseModel):
    user_id: int = Field(..., description="사용자의 고유 ID")
    username: str = Field(..., description="사용자의 이름")
    useremail: EmailStr = Field(..., description="사용자의 이메일 주소")
    profile_image: str = Field(default=None, description="사용자의 프로필 이미지 URL")
    location: str = Field(..., max_length=100, description="사용자의 위치")
    created_at: datetime = Field(..., description="계정 생성 시간")

    # 비밀번호 일치 검증 메서드 추가
    def password_match(self, password: str, password_confirm: str) -> bool:
        return password == password_confirm
    
class UserInDB(User):
    hashed_password: str = Field(..., description="해시된 비밀번호")

# Admin 모델
class Admin(BaseModel):
    adminname: Optional[str] = Field(default="관리자", description="Admin 닉네임")
    adminemail: EmailStr = Field(..., description="Admin 고유 이메일")
    adminpassword: str = Field(..., description="Admin 비밀번호")
    adminpassword_confirm: str = Field(..., alias="adminpasswordConfirm", description="Admin 비밀번호 확인")

    def password_match(self) -> bool:
        return self.adminpassword == self.adminpassword_confirm

class AdminInDB(Admin):
    hashed_password: str = Field(..., description="해시된 Admin 비밀번호")

# 토큰 모델
class Token(BaseModel):
    access_token: str = Field(..., description="접근 토큰")
    token_type: str = Field(..., description="토큰 유형")
    email: Optional[str] = Field(None, description="이메일 주소")

class TokenData(BaseModel):
    email: Optional[str] = Field(None, description="이메일 주소")

class TokenBlacklist(BaseModel):
    jti: str = Field(..., description="토큰 식별자 (JTI)")
    exp: datetime = Field(..., description="토큰 만료 시간")