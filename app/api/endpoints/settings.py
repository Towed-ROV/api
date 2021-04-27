import time
from typing import List

from crud import crud
from db.database import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from schemas.setting import Setting, SettingCreate, SettingUpdate
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=Setting)
def create_setting(setting: SettingCreate, db: Session = Depends(get_db)):
    db_setting = crud.get_setting_by_name(db, setting.name)
    if db_setting:
        raise HTTPException(status_code=400 , detail=f"Setting already exist")
    return crud.create_setting(db, setting=setting)

@router.get("/", response_model=List[Setting])
def get_settings(db: Session = Depends(get_db)):
    return crud.get_settings(db)

@router.get("/{id}", response_model=Setting)
def get_setting(id: int, db: Session = Depends(get_db)):
    return crud.get_setting(db, id)


@router.put("/{name}", response_model=Setting)
def update_setting_by_name(setting: SettingUpdate, db: Session = Depends(get_db)):
    return crud.update_setting(db, setting)

@router.delete("/{id}", response_model=Setting)
def delete_setting(id: int, db: Session = Depends(get_db)):
    return crud.delete_setting(db, id)
