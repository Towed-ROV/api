from fastapi import APIRouter
from api.endpoints import videos, commands, sensors

api_router = APIRouter()
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(commands.router, prefix="/commands", tags=["commands"])
api_router.include_router(sensors.router, prefix="/sensors", tags=["sensors"])


