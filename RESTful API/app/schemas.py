from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DeviceBase(BaseModel):
    device_name: str

class DeviceResponse(DeviceBase):
    id: int
    class Config:
        orm_mode = True

class ResultBase(BaseModel):
    id: str
    data: List[str]
    device_name: str

class ResultResponse(BaseModel):
    id: str
    average_before: float
    average_after: float
    data_size: int
    created_date: datetime
    updated_date: datetime
    device: DeviceResponse
    class Config:
        orm_mode = True
