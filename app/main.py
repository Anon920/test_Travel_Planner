from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import TravelProject
from app.schemas import TravelProjectCreate, TravelProjectRead, TravelProjectUpdate

app = FastAPI(title="Travel Planner API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Travel Planner API is running"}

@app.post("/projects", response_model=TravelProjectRead, status_code=201)
def create_project(project_data: TravelProjectCreate, db: Session = Depends(get_db)):
    project = TravelProject(**project_data.model_dump())

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@app.get("/projects", response_model=list[TravelProjectRead])
def list_projects(db: Session = Depends(get_db)):
    return db.query(TravelProject).all()

@app.get("/projects/{project_id}", response_model=TravelProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(TravelProject).filter(TravelProject.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@app.patch("/places/{project_id}", response_model=TravelProjectRead)
def update_project(project_id:int, project_data: TravelProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(TravelProject).filter(TravelProject.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project

@app.delete("/places/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(TravelProject).filter(TravelProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return "Project deleted successfully"