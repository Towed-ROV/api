from schemas.waypoint_session import WaypointSession, WaypointSessionCreate
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from typing import List
from crud import crud
import time

router = APIRouter()


@router.get("/{session_id}", response_model=WaypointSession)
def get_waypoint_session(session_id: str, db: Session = Depends(get_db)):
    session = crud.get_waypoint_session(db, session_id=session_id)
    if not session:
        raise HTTPException(
            status_code=404, detail=f"Session ID: [{session_id}] not found")
    return session


@router.get("/", response_model=List[WaypointSession])
def get_settings(db: Session = Depends(get_db)):
    # TODO: Add range
    return crud.get_waypoint_sessions(db)


@router.post("/", response_model=Setting)
def create_setting(waypoint_session: WaypointSessionCreate, db: Session = Depends(get_db)):
    return crud.create_waypoint_session(db, waypoint_session=waypoint_session)
