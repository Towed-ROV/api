from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from db.base_class import Base


class WaypointSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    is_complete = Column(Boolean, unique=False, default=False, nullable=False)

    # waypoints = relationship("Waypoint", back_populates="owner", cascade="all, delete-orphan")
