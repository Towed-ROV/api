from pydantic import BaseModel

class Command(BaseModel):
    name: str
    value: float
    toSystem: bool
    