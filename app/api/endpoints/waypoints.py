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

@router.get("/", response_model=List[Waypoint])
def get_waypoints(db: Session = Depends(get_db)):
    waypoints = crud.get_waypoints(db)
    if not waypoints:
        raise HTTPException(status_code=404, detail="Waypoints not found")
    return waypoints

@router.post("/", response_model=Waypoint)
def create_waypoint(ab_way: AbstractWaypoint, db: Session = Depends(get_db)):
    # TODO: Do better, remove abstraction
    return crud.create_waypoint(
        db,
        sess_id=ab_way.session_id,
        lat=ab_way.latitude,
        lng=ab_way.longitude,
        sensors=ab_way.sensors)

@router.get("/{session_id}", response_model=List[Waypoint])
def get_waypoints_by_session_id(session_id: str, db: Session = Depends(get_db)):
    waypoints = crud.get_waypoints_by_session_id(db, session_id=session_id)
    if not waypoints:
        raise HTTPException(status_code=404, detail="Waypoints not found")
    return waypoints
