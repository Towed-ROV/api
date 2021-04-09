from schemas.waypoint import Waypoint, WaypointCreate, AbstractWaypoint
from schemas.sensor import Sensor, SensorCreate, SensorList
from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from typing import List
from crud import crud

router = APIRouter()

@router.get("/{waypoint_id}", response_model=Waypoint)
def get_waypoint(waypoint_id: int, db: Session = Depends(get_db)):
    waypoint = crud.get_waypoint(db, waypoint_id=waypoint_id)
    if not waypoint:
        raise HTTPException(status_code=404, detail=f"Waypoint [{waypoint_id}] not found")
    return waypoint

@router.get("/", response_model=List[Waypoint])
def get_multiple_waypoints(db: Session = Depends(get_db)):
    waypoints = crud.get_waypoints(db)
    if not waypoints:
        raise HTTPException(status_code=404, detail="Waypoints not found")
    return waypoints

@router.get("/{session_id}", response_model=List[Waypoint])
def get_waypoints_by_session_id(session_id: str, db: Session = Depends(get_db)):
    waypoints = crud.get_waypoints_by_session_id(db, session_id=session_id)
    if not waypoints:
        raise HTTPException(status_code=404, detail="Waypoints not found")
    return waypoints

@router.post("/", response_model=Waypoint)
def create_waypoint(waypoint: AbstractWaypoint, db: Session = Depends(get_db)):
    # TODO: Do better, remove abstraction
    return crud.create_waypoint(
        db,
        sess_id=waypoint.session_id,
        lat=waypoint.latitude,
        lng=waypoint.longitude,
        sensors=waypoint.sensors)

@router.delete("/{session_id}")
def delete_waypoints_by_session_id(session_id: str, db: Session = Depends(get_db)):
    response = crud.delete_waypoints_by_session_id(db, session_id=session_id)
    if response["code"] == 404: raise HTTPException(status_code=404, detail="Session not found")
    elif response["code"] == 200: return {"message": f"Successfully deleted session: {session_id}"}