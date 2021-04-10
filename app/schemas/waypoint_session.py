from pydantic import BaseModel
from typing import List


class WaypointSessionBase(BaseModel):
    session_id: str


class WaypointSessionCreate(WaypointSessionBase):
    created_at: str


class WaypointSession(WaypointSessionBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class WaypointSessionList(WaypointSessionBase):
    l: List[WaypointSession]
