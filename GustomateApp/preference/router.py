from ..database import models 
from . import schema 
from . import CRUD as crud 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependency.dependencies import get_db 


router = APIRouter(
    prefix="/preferences",
    tags=["preferences"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schema.UserPreference, status_code=201)
def add_user_preference(preference: schema.UserPreferenceCreate, db: Session = Depends(get_db)):
    # Ensure the user_id exists in the users table
    user = db.query(models.User).filter(models.User.user_id == preference.user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.create_user_preference(db=db, preference=preference)

@router.get("/{user_id}", response_model=schema.UserPreference)
def read_user_preference(user_id: int, db: Session = Depends(get_db)):
    preference = crud.get_user_preference(db=db, user_id=user_id)
    if preference is None:
        raise HTTPException(status_code=404, detail="User preference not found")
    return preference

@router.put("/{user_id}", response_model=schema.UserPreference)
def update_user_preference(user_id: int, preference: schema.UserPreferenceUpdate, db: Session = Depends(get_db)):
    db_preference = crud.update_user_preference(db=db, user_id=user_id, preference=preference)
    if db_preference is None:
        raise HTTPException(status_code=404, detail="User preference not found")
    return db_preference

@router.delete("/{user_id}", status_code=204)
def delete_user_preference(user_id: int, db: Session = Depends(get_db)):
    db_preference = crud.get_user_preference(db, user_id=user_id)
    if db_preference is None:
        raise HTTPException(status_code=404, detail="User preference not found")
    crud.delete_user_preference(db=db, user_id=user_id)
    return {"message": "User preference deleted successfully"}