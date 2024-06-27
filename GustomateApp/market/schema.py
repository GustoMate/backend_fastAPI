from pydantic import BaseModel, Field
from datetime import datetime

# Market: Market 정보
class Market(BaseModel):
    market_id: int = Field(..., description="마켓의 고유 ID")
    user_id: int = Field(..., description="마켓을 등록한 사용자의 ID")
    ingredient_id: int = Field(..., description="마켓에 등록된 재료의 ID")
    market_image: str = Field(..., description="마켓 이미지 URL")
    market_description: str = Field(..., description="마켓 설명")
    created_at: datetime = Field(..., description="마켓 생성 시간")
    updated_at: datetime = Field(..., description="마켓 수정 시간")

# MarketCreate: Market 생성 시 필요한 정보
class MarketCreate(BaseModel):
    user_id: int = Field(..., description="마켓을 등록한 사용자의 ID")
    ingredient_id: int = Field(..., description="마켓에 등록된 재료의 ID")
    market_image: str = Field(..., description="마켓 이미지 URL")
    market_description: str = Field(..., description="마켓 설명")
    created_at: datetime = Field(..., description="마켓 생성 시간")
    updated_at: datetime = Field(..., description="마켓 수정 시간")

# MarketUpdate: Market 수정 시 필요한 정보
class MarketUpdate(BaseModel):
    market_id: int = Field(..., description="마켓의 고유 ID")
    user_id: int = Field(..., description="마켓을 등록한 사용자의 ID")
    ingredient_id: int = Field(..., description="마켓에 등록된 재료의 ID")
    market_image: str = Field(..., description="마켓 이미지 URL")
    market_description: str = Field(..., description="마켓 설명")
    updated_at: datetime = Field(..., description="마켓 수정 시간")

# MarketDelete: Market 삭제 시 필요한 정보
class MarketDelete(BaseModel):
    market_id: int = Field(..., description="마켓의 고유 ID")
    user_id: int = Field(..., description="마켓을 등록한 사용자의 ID")
    ingredient_id: int = Field(..., description="마켓에 등록된 재료의 ID")
    market_image: str = Field(..., description="마켓 이미지 URL")
    market_description: str = Field(..., description="마켓 설명")
    updated_at: datetime = Field(..., description="마켓 수정 시간")