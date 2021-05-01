from pydantic import BaseModel
from typing import Optional


class SettingBase(BaseModel):
    name: str
    enabled: bool
    origin: str
    role: str
    port: str


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingBase):
    id: Optional[int]
    name: Optional[str]
    enabled: Optional[bool]
    origin: Optional[str]
    role: Optional[str]
    port: Optional[str]


class Setting(SettingBase):
    id: int

    class Config:
        orm_mode = True
