from typing import Optional
from datetime import date

from pydantic.v1 import BaseModel


class TravelProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

class TravelProjectCreate(TravelProjectBase):
    pass

class TravelProjectUpdate(TravelProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None

class TravelProjectRead(TravelProjectBase):
    id: int
    is_completed: bool

    class Config:
        from_attributes = True
