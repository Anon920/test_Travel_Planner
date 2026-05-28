from fastapi import FastAPI

app = FastAPI()

@app.post("/projects")
def projects():
    return {"message": "Travel Planner API is running"}

@app.get("/projects")
def projects():
    return {"message": "Travel Planner API is running"}

@app.get("/projects/{project_id}")
def projects(project_id):
    return {"message": "Travel Planner API is running"}

@app.patch("/places/{project_id}")
def places(project_id):
    return {"message": "Travel Planner API is running"}

@app.delete("/places/{project_id}")
def places(project_id):
    return {"message": "Travel Planner API is running"}