from sqlalchemy.orm import Session
from ..database.models import Market
from .schema import MarketCreate, MarketUpdate, MarketDelete

# Market 생성
def create_market(db: Session, market: MarketCreate):
    db_market = Market(**market.dict())
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market

# Market 조회
def get_market(db: Session, market_id: int):
    return db.query(Market).filter(Market.market_id == market_id).first()

# Market 전체 조회
def get_markets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Market).offset(skip).limit(limit).all()

# Market 수정
def update_market(db: Session, market: MarketUpdate):
    db.query(Market).filter(Market.market_id == market.market_id).update(market.dict())
    db.commit()
    return db.query(Market).filter(Market.market_id == market.market_id).first()

# Market 삭제
def delete_market(db: Session, market: MarketDelete):
    db.query(Market).filter(Market.market_id == market.market_id).delete()
    db.commit()
    return market.market_id



