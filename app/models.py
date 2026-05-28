from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class TravelProject(Base):
    __tablename__ = "travel_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    start_date = Column(Date)
    is_closed = Column(Boolean, default=False)

    places = relationship("ProjectPlace", back_populates="project")

class ProjectPlace(Base):
    __tablename__ = "project_places"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('travel_projects.id'))
    external_id = Column(Integer)
    title = Column(String)
    notes = Column(String)
    visited = Column(Boolean)

    places = relationship("TravelProject", back_populates="places")

