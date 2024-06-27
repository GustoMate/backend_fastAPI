from sqlalchemy.orm import Session
from . import schema as schemas
from ..database import models
import json

def create_user_preference(db: Session, preference: schemas.UserPreferenceCreate, user_id: int):
    db_preference = models.UserPreference(**preference.dict(), user_id=user_id)
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference

def get_user_preference(db: Session, user_id: int):
    db_preference = db.query(models.UserPreference).filter(models.UserPreference.user_id == user_id).first()
    if db_preference:
        db_preference.allergies = json.loads(db_preference.allergies)
    return db_preference

def update_user_preference(db: Session, user_id: int, preference: schemas.UserPreferenceUpdate):
    db_preference = get_user_preference(db, user_id)
    if db_preference:
        for key, value in preference.dict().items():
            if key == 'allergies':
                value = json.dumps(value)
            setattr(db_preference, key, value)
        db.commit()
        db.refresh(db_preference)
        db_preference.allergies = json.loads(db_preference.allergies)
    return db_preference

def delete_user_preference(db: Session, user_id: int):
    db_preference = get_user_preference(db, user_id)
    if db_preference:
        db.delete(db_preference)
        db.commit()
    return db_preference
