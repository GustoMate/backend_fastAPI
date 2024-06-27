from pydantic import BaseModel
from datetime import datetime

# MarketListRequest: 시장에 재료 등록 요청 정보
class MarketListRequest(BaseModel):
    ingredient_id: int
    description: str

# MarketListResponse: 시장에 등록된 재료 응답 정보
class MarketListResponse(BaseModel):
    id: int
    user_id: int
    ingredient_id: int
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True