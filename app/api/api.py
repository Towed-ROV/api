from fastapi import APIRouter
# from api.endpoints import sensors, commands, videos
from api.endpoints import waypoints, waypoint_sessions, videos

api_router = APIRouter()
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
# api_router.include_router(commands.router, prefix="/commands", tags=["commands"])
# api_router.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
api_router.include_router(waypoints.router, prefix="/waypoints", tags=["waypoints"])
api_router.include_router(waypoint_sessions.router, prefix="/waypoint_sessions", tags=["waypoint_sessions"])
# api_router.include_router(settings.router, prefix="/settings", tags=["settings"])



