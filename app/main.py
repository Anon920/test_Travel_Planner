from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.external_api import get_word_by_id
from app.models import TravelProject, ProjectPlace
from app.schemas import TravelProjectCreate, TravelProjectRead, TravelProjectUpdate, ProjectPlaceRead, \
    ProjectPlaceCreate

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

@app.post("/projects/{project_id}/places", response_model=ProjectPlaceRead, status_code=201)
def add_place_to_project(project_id: int, place_data: ProjectPlaceCreate, db: Session = Depends(get_db)):

    project = db.query(TravelProject).filter(TravelProject.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    places_count = (db.query(TravelProject).filter(TravelProject.id == project_id).count())

    if places_count >= 10:
        raise HTTPException(status_code=400, detail="Project cannot have more than 10 places")

    existing_place = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.project_id == project_id,
            ProjectPlace.external_id == place_data.external_id
        ).first())

    if existing_place:
        raise HTTPException(status_code=400, detail="This place already exists in the project")

    work = get_word_by_id(place_data.external_id)

    if not work:
        raise HTTPException(status_code=400, detail="Place not found in external API")

    place = ProjectPlace(
        project_id=project_id,
        external_id=work["external_id"],
        title=work["title"],
        notes=place_data.notes,
    )

    db.add(place)
    db.commit()
    db.refresh(place)

    return place

@app.get(
    "/projects/{project_id}/places",
    response_model=list[ProjectPlaceRead],
)
def list_project_places(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = db.query(TravelProject).filter(TravelProject.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return db.query(ProjectPlace).filter(ProjectPlace.project_id == project_id).all()


@app.get(
    "/projects/{project_id}/places/{place_id}",
    response_model=ProjectPlaceRead,
)
def get_project_place(
    project_id: int,
    place_id: int,
    db: Session = Depends(get_db),
):
    place = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.id == place_id,
            ProjectPlace.project_id == project_id,
        )
        .first()
    )

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    return place


@app.patch(
    "/projects/{project_id}/places/{place_id}",
    response_model=ProjectPlaceRead,
)
def update_project_place(
    project_id: int,
    place_id: int,
    place_data: ProjectPlaceUpdate,
    db: Session = Depends(get_db),
):
    place = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.id == place_id,
            ProjectPlace.project_id == project_id,
        )
        .first()
    )

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    update_data = place_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(place, field, value)

    db.commit()
    db.refresh(place)

    project_places = (
        db.query(ProjectPlace)
        .filter(ProjectPlace.project_id == project_id)
        .all()
    )

    project = db.query(TravelProject).filter(TravelProject.id == project_id).first()

    if project_places and all(project_place.visited for project_place in project_places):
        project.is_completed = True
    else:
        project.is_completed = False

    db.commit()
    db.refresh(place)

    return place
