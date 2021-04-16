from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base_class import Base


class Waypoint(Base):
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String)
    img_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    sensors = relationship("Sensor", back_populates="wp",
                           cascade="all, delete-orphan")

