from fastapi import FastAPI
from models import Developer,Projekt

app =FastAPI()

@app.post("/developers/")
def developer(developer: Developer):
    return {"mesage":"Developer was created sucesfully","developer":developer}

@app.post("/projects/")
def project(project: Projekt):
    return {"mesage":"Project was created sucesfully","project":project}

@app.get("/projects/")
def get_projects():
    sample_projects=Projekt(
        title:"Sample project",
        description:"Sample description",

    )