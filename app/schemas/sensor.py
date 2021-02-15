from pydantic import BaseModel

class Sensor(BaseModel):
    name: str
    value: int
    description: Optional[str] = None