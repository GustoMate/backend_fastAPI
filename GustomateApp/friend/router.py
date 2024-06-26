from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import FriendDetail
from .CRUD import get_friends
from starlette.requests import Request
from ..dependency.dependencies import get_db, get_current_user, get_token_from_session
from ..database import models

router = APIRouter(prefix="/friends", tags=["friends"])

# 친구 목록
@router.get("", response_model=List[FriendDetail])
async def read_friends(request: Request, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    # 세션에서 토큰을 가져옵니다
    token = await get_token_from_session(request)
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    # 현재 로그인된 사용자 정보를 가져옵니다
    user_friends = get_friends(db, current_user.user_id)
    return user_friends
