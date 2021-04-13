from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class WaypointSessionBase(BaseModel):
    session_id: str


class WaypointSessionCreate(WaypointSessionBase):
    pass

class WaypointSessionUpdate(WaypointSessionBase):
    is_complete: Optional[bool]

class WaypointSession(WaypointSessionBase):
    id: int
    created_at: datetime
    is_complete: bool
    # owner_id: int

    class Config:
        orm_mode = True


class WaypointSessionList(WaypointSessionBase):
    l: List[WaypointSession]
