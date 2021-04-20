from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class Setting(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    origin = Column(String)
    role = Column(String)
    port = Column(String)