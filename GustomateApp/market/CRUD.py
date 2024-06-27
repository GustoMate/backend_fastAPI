from sqlalchemy.orm import Session
from ..database.models import Market
from .schema import MarketlistRequest, MarketListResponse

def create_market_list(db: Session, market: MarketlistRequest, user_id: int):
    db_market = Market(user_id=user_id, ingredient_id=market.ingredient_id, description=market.description)
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market

def update_market_list(db: Session, list_id: int, market: MarketlistRequest):
    db_market = db.query(Market).filter(Market.id == list_id).first()
    if db_market:
        db_market.ingredient_id = market.ingredient_id
        db_market.description = market.description
        db.commit()
        db.refresh(db_market)
    return db_market

def delete_market_list(db: Session, list_id: int):
    db_market = db.query(Market).filter(Market.id == list_id).first()
    if db_market:
        db.delete(db_market)
        db.commit()
    return db_market
