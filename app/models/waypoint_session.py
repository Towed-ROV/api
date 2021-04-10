from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db.base_class import Base


class WaypointSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # waypoints = relationship("Waypoint", back_populates="owner", cascade="all, delete-orphan")
