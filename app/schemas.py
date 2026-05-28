from typing import Optional
from datetime import date

from pydantic import ConfigDict, BaseModel


class TravelProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

class TravelProjectCreate(TravelProjectBase):
    pass

class TravelProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None

class TravelProjectRead(TravelProjectBase):
    id: int
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)

class ProjectPlace(BaseModel):
    external_id: int
    notes: Optional[str]

class ProjectPlaceCreate(ProjectPlace):
    pass

class ProjectPlaceUpdate(ProjectPlace):
    notes: Optional[str] = None
    visited: Optional[bool] = None

class ProjectPlaceRead(ProjectPlace):
    id: int
    project_id: int
    external_id: int
    title: str
    notes: Optional[str] = None
    visited: bool

    model_config = ConfigDict(from_attributes=True)

