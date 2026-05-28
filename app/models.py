from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class TravelProject(Base):
    __tablename__ = "travel_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=False)

    places = relationship("ProjectPlace", back_populates="project")

class ProjectPlace(Base):
    __tablename__ = "project_places"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("travel_projects.id"), nullable=False)
    external_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    visited = Column(Boolean, default=False)

    project = relationship("TravelProject", back_populates="places")

