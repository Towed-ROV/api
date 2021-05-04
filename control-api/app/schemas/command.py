from typing import Optional
from pydantic import BaseModel


class Command(BaseModel):
    name: Optional[str]
    value: Optional[float]
    origin: Optional[str]
    port: Optional[str]
    toSystem: bool
    config: bool
