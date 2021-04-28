from pydantic import BaseModel


class VideoPreference(BaseModel):
    action: str
    display_mode: str
