from sqlalchemy.orm import Session
from . import schema as schemas
from ..database import models
import json

HARDCODED_USER_ID = 1

def create_user_preference(db: Session, preference: schemas.UserPreferenceCreate):
    try:
        db_preference = models.UserPreference(**preference.dict(), user_id=HARDCODED_USER_ID)
        db.add(db_preference)
        db.commit()
        db.refresh(db_preference)
        return db_preference
    except Exception as e:
        raise Exception(f"Error creating user preference: {e}")

def get_user_preference(db: Session):
    try:
        db_preference = db.query(models.UserPreference).filter(models.UserPreference.user_id == HARDCODED_USER_ID).first()
        if db_preference:
            try:
                db_preference.allergies = json.loads(db_preference.allergies) if db_preference.allergies else []
            except json.JSONDecodeError:
                db_preference.allergies = []
        return db_preference
    except Exception as e:
        raise Exception(f"Error getting user preference: {e}")

def update_user_preference(db: Session, preference: schemas.UserPreferenceUpdate):
    try:
        db_preference = get_user_preference(db)
        if db_preference:
            for key, value in preference.dict().items():
                if key == 'allergies':
                    value = json.dumps(value)
                setattr(db_preference, key, value)
            db.commit()
            db.refresh(db_preference)
            db_preference.allergies = json.loads(db_preference.allergies)
        return db_preference
    except Exception as e:
        raise Exception(f"Error updating user preference: {e}")

def delete_user_preference(db: Session):
    try:
        db_preference = get_user_preference(db)
        if db_preference:
            db.delete(db_preference)
            db.commit()
        return db_preference
    except Exception as e:
        raise Exception(f"Error deleting user preference: {e}")
