from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    origin = Column(String, index=True)