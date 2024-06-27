from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import Market
from .CRUD import get_markets, get_market, update_market, create_market, update_market, delete_market
from ..dependency.dependencies import get_db 

router = APIRouter(prefix="/market", tags=["market"])

# market 글 전체 조회
@router.get("", response_model=List[Market])
async def get_market_list(skip: int = 0, limit: int = 6, db: Session = Depends(get_db)):
    markets = get_markets(db, skip=skip, limit=limit)
    return markets

# market 글 상세 조회
@router.get("/{market_id}", response_model=Market)
async def get_market_detail(market_id: int, db: Session = Depends(get_db)):
    db_market = get_market(db, market_id)
    if db_market is None:
        raise HTTPException(status_code=404, detail="market post not found")
    return db_market

# market 글 작성
@router.post("", response_model=Market)
async def post_market(market: Market, db: Session = Depends(get_db)):
    return create_market(db, market)

# market 글 수정
@router.put("/{market_id}", response_model=Market)
async def put_market(market_id: int, market: Market, db: Session = Depends(get_db)):
    db_market = update_market(db, market_id, market)
    if db_market is None:
        raise HTTPException(status_code=404, detail="market post not found")
    return db_market

# market 글 삭제
@router.delete("/{market_id}", response_model=Market)
async def delete_market(market_id: int, db: Session = Depends(get_db)):
    db_market = delete_market(db, market_id)
    if db_market is None:
        raise HTTPException(status_code=404, detail="market post not found")
    return db_market



"""
# market 글 작성
@router.post("/market", response_model=schemas.MarketlistResponse)
async def post_market(list: schemas.MarketlistRequest, db: Session = Depends(get_db), user_id: int = 1):
    return create_market_list(db, list, user_id)

@router.put("/market/{market_id}", response_model=schemas.MarketlistResponse)
async def update_market(market_id: int, list: schemas.MarketlistRequest, db: Session = Depends(get_db)):
    db_market = update_market_list(db, market_id, list)
    if db_market is None:
        raise HTTPException(status_code=404, detail="market post not found")
    return db_market

@router.delete("/market/{market_id}", response_model=schemas.MarketlistResponse)
async def delete_market(market_id: int, db: Session = Depends(get_db)):
    db_market = delete_market_list(db, market_id)
    if db_market is None:
        raise HTTPException(status_code=404, detail="market post not found")
    return db_market
"""