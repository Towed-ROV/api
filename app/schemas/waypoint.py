from typing import Dict, List

from pydantic import BaseModel

from schemas.sensor import Sensor


class WaypointBase(BaseModel):
    session_id: str
    img_name: str
    latitude: float
    longitude: float


class WaypointCreate(WaypointBase):
    pass


class Waypoint(WaypointBase):
    id: int
    sensors: List[Sensor]

    class Config:
        orm_mode = True


class AbstractWaypoint(BaseModel):
    session_id: str
    latitude: float
    longitude: float
    sensors: List[Dict]
