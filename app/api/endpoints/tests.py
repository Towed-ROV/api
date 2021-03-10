from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Request
from typing import List
from pydantic import BaseModel

router = APIRouter()

settings = [
    {
        "name": "temperature",
        "origin": "arduino_1",
        "role": "pub",
        "port": "d11"
    },
    {
        "name": "set_point",
        "origin": "arduino_2",
        "role": "pubsub",
        "port": "d1"
    },
    {
        "name": "oxygen",
        "origin": "arduino_2",
        "role": "pub",
        "port": "a3"
    },
    {
        "name": "pressure",
        "origin": "arduino_1",
        "role": "pub",
        "port": "a4"
    },
]

class SensorSetting(BaseModel):
    name: str
    origin: str
    role: str
    port: str

@router.post("/settings")
def post_cmd(sensor_settings: List[SensorSetting]):
    for sensor_setting in sensor_settings:
        print("")
        print(sensor_setting)
        print("")
    return {"code": "success"}

@router.get("/settings")
def post_cmd():
    global settings
    return settings

