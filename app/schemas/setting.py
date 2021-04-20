from pydantic import BaseModel
from typing import Optional


class SettingBase(BaseModel):
    name: str
    origin: str
    role: str
    port: str

class SettingCreate(SettingBase):
    pass

class SettingUpdate(SettingBase):
    name: str
    origin: Optional[str]
    role: Optional[str]
    port: Optional[str]

class Setting(SettingBase):
    id: int
    
    class Config:
        orm_mode = True
