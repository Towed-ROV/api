from schemas.setting import Setting, SettingCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from typing import List
from crud import crud
import time

router = APIRouter()

@router.get("/", response_model=List[Setting])
def get_settings(db: Session = Depends(get_db)):
    return crud.get_settings(db)

@router.post("/", response_model=Setting)
def create_setting(setting: SettingCreate, db: Session = Depends(get_db)):
    return crud.create_setting(db, setting=setting)