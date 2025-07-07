from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String, unique=True, index=True)

class ResultEntry(Base):
    __tablename__ = "results"
    id = Column(String, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    average_before = Column(Float)
    average_after = Column(Float)
    data_size = Column(Integer)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    device = relationship("Device")
