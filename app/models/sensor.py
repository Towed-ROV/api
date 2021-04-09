from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base_class import Base

class Sensor(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    value = Column(Float)
    owner_id = Column(Integer, ForeignKey("waypoints.id"), nullable=False)
    owner = relationship("Waypoint", back_populates="sensors")    

    