from db.base_class import Base
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship


class Waypoint(Base):
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String)
    img_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    sensors = relationship("Sensor", back_populates="wp",
                           cascade="all, delete-orphan")
