from pydantic import BaseModel
from typing import List


class SensorBase(BaseModel):
    name: str
    value: float
class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    id: int
    wp_id: int
    class Config:
        orm_mode = True
class SensorList(SensorBase):
    l: List[Sensor]