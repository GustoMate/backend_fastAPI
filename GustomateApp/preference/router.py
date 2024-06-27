from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import models
from . import schema
from . import CRUD as crud
from ..dependency.dependencies import get_db

router = APIRouter(
    prefix="/preferences",
    tags=["preferences"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=schema.UserPreference, status_code=201)
async def add_user_preference(preference: schema.UserPreferenceCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user_preference(db=db, preference=preference)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding user preference: {str(e)}")

@router.get("", response_model=schema.UserPreference)
async def read_user_preference(db: Session = Depends(get_db)):
    try:
        preference = crud.get_user_preference(db=db)
        if preference is None:
            raise HTTPException(status_code=404, detail="User preference not found")
        return preference
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading user preference: {str(e)}")

@router.put("", response_model=schema.UserPreference)
async def update_user_preference(preference: schema.UserPreferenceUpdate, db: Session = Depends(get_db)):
    try:
        db_preference = crud.update_user_preference(db=db, preference=preference)
        if db_preference is None:
            raise HTTPException(status_code=404, detail="User preference not found")
        return db_preference
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user preference: {str(e)}")

@router.delete("", status_code=204)
async def delete_user_preference(db: Session = Depends(get_db)):
    try:
        db_preference = crud.get_user_preference(db)
        if db_preference is None:
            raise HTTPException(status_code=404, detail="User preference not found")
        crud.delete_user_preference(db=db)
        return {"message": "User preference deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user preference: {str(e)}")
