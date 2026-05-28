from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Travel Planner API is running"}

@app.post("/projects")
def projects():
    return {"message": "Travel Planner API is running"}

@app.get("/projects")
def projects():
    return {"message": "Travel Planner API is running"}