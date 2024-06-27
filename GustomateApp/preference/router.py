from ..database import models 
from . import schema 
from . import CRUD as crud 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependency.dependencies import get_db, get_current_user


router = APIRouter(
    prefix="/preferences",
    tags=["preferences"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=schema.UserPreference, status_code=201)
async def add_user_preference(preference: schema.UserPreferenceCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    # Ensure the user_id exists in the users table
    user = db.query(models.Users).filter(models.Users.user_id == current_user.user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.create_user_preference(db=db, preference=preference, user_id=current_user.user_id)

@router.get("", response_model=schema.UserPreference)
async def read_user_preference(db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    preference = crud.get_user_preference(db=db, user_id=current_user.user_id)
    if preference is None:
        raise HTTPException(status_code=404, detail="User preference not found")
    return preference

@router.put("", response_model=schema.UserPreference)
async def update_user_preference(preference: schema.UserPreferenceUpdate, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    db_preference = crud.update_user_preference(db=db, user_id=current_user.user_id, preference=preference)
    if db_preference is None:
        raise HTTPException(status_code=404, detail="User preference not found")
    return db_preference

@router.delete("", status_code=204)
async def delete_user_preference(db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    db_preference = crud.get_user_preference(db, user_id=current_user.user_id)
    if db_preference is None:
        raise HTTPException(status_code=404, detail="User preference not found")
    crud.delete_user_preference(db=db, user_id=current_user.user_id)
    return {"message": "User preference deleted successfully"}
