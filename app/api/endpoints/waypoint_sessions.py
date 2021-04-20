from schemas.waypoint_session import WaypointSession, WaypointSessionCreate, WaypointSessionUpdate
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from typing import List
from crud import crud
import time
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post("/", response_model=WaypointSession)
def create_waypoint_session(waypoint_session: WaypointSessionCreate, db: Session = Depends(get_db)):
    session = crud.get_waypoint_session(db, session_id=waypoint_session.session_id)
    if session:
        raise HTTPException(status_code=400 , detail=f"Waypointsession already exist")
    return crud.create_waypoint_session(db, waypoint_session=waypoint_session)

@router.get("/completed", response_model=List[WaypointSession])
def get_completed_waypoint_sessions(db: Session = Depends(get_db)):
    is_complete: bool = True
    waypoints_sessions = crud.get_complete_waypoint_sessions(db, is_complete)
    if not waypoints_sessions:
        raise HTTPException(status_code=404, detail="Waypointsession(s) not found.")
    return waypoints_sessions

@router.get("/uncompleted", response_model=List[WaypointSession])
def get_uncompleted_waypoint_sessions(db: Session = Depends(get_db)):
    is_complete: bool = False
    waypoints_sessions = crud.get_complete_waypoint_sessions(db, is_complete)
    if not waypoints_sessions:
        raise HTTPException(status_code=404, detail="Waypointsession(s) not found.")
    return waypoints_sessions

@router.get("/{session_id}", response_model=WaypointSession)
def get_waypoint_session(session_id: str, db: Session = Depends(get_db)):
    session = crud.get_waypoint_session(db, session_id=session_id)
    if not session:
        raise HTTPException(
            status_code=404, detail=f"Waypointsession [{session_id}] not found")
    return session

@router.get("/", response_model=List[WaypointSession])
def get_multiple_waypoint_sessions(db: Session = Depends(get_db)):
    waypoints_sessions = crud.get_waypoint_sessions(db)
    if not waypoints_sessions:
        raise HTTPException(status_code=404, detail="No waypointsessions in database.")
    return waypoints_sessions

        
@router.put("/{session_id}", response_model=WaypointSession)
def update_waypoint_session(waypoint_session: WaypointSessionUpdate, db: Session = Depends(get_db)):
    session = crud.update_waypoint_session(db, waypoint_session)
    if not session:
        raise HTTPException(
            status_code=404, detail=f"Could not update session")
    return session

@router.delete("/{session_id}")
def delete_waypoint_session_by_session_id(session_id: str, db: Session = Depends(get_db)):
    response = crud.delete_waypoint_session_by_session_id(db, session_id=session_id)
    if response["code"] == 404: raise HTTPException(status_code=404, detail="WaypointSession not found")
    elif response["code"] == 200: return {"message": f"Successfully deleted WaypointSession: {session_id}"}