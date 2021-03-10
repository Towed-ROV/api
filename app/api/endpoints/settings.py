from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Request, Depends
from db.session import SessionLocal
from typing import List, Generator
from sqlalchemy.orm import Session
from pydantic import BaseModel
from crud import crud
from schemas.setting import Setting, SettingCreate

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/", response_model=List[Setting])
def get_settings(db: Session = Depends(get_db)):
    return crud.get_settings(db)

@router.post("/", response_model=Setting)
def create_setting(setting: SettingCreate, db: Session = Depends(get_db)):
    return crud.create_setting(db, setting=setting)