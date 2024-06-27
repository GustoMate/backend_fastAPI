from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import *
from .CRUD import *
from ..dependency.dependencies import get_db 

router = APIRouter()

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
