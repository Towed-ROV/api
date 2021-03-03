from pydantic import BaseModel

class Sensor(BaseModel):
    name: str
    value: int