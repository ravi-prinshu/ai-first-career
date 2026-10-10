from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()
class ProjectCreate(BaseModel):
    project_name: str
    status: str
    cost: int
    delay_days: int

class ProjectUpdate(BaseModel):
    project_name: str
    status: str
    cost: int
    delay_days: int


@app.get("/hello")
def hello():
    return {"message": "Hello Ravi"}


@app.get("/about")
def about():
    return {
        "name": "Ravi",
        "role": "AI-First Learner"
    }



def get_project_from_db(project_id: int):
    connection = sqlite3.connect("september/week2/portfolio.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM projects WHERE project_id = ?",
        (project_id,)
    )

    project = cursor.fetchone()

    connection.close()

    return project

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    project = get_project_from_db(project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "project_id": project[0],
        "project_name": project[1],
        "status": project[2],
        "cost": project[3],
        "delay_days": project[4]
    }

@app.get("/projects")
def get_projects(status: str | None = None):
    connection = sqlite3.connect("september/week2/portfolio.db")
    cursor = connection.cursor()

    if status is None:
        cursor.execute("SELECT * FROM projects")
    else:
        cursor.execute(
            "SELECT * FROM projects WHERE status = ?",
            (status,)
        )

    projects = cursor.fetchall()

    connection.close()

    return [
        {
            "project_id": project[0],
            "project_name": project[1],
            "status": project[2],
            "cost": project[3],
            "delay_days": project[4]
        }
        for project in projects
    ]

@app.post("/projects")
def create_project(project: ProjectCreate):
    connection = sqlite3.connect("september/week2/portfolio.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO projects
        (project_name, status, cost, delay_days)
        VALUES (?, ?, ?, ?)
        """,
        (
            project.project_name,
            project.status,
            project.cost,
            project.delay_days
        )
    )

    connection.commit()

    project_id = cursor.lastrowid

    connection.close()

    return {
        "project_id": project_id,
        "project_name": project.project_name,
        "status": project.status,
        "cost": project.cost,
        "delay_days": project.delay_days
    }

@app.put("/projects/{project_id}")
def update_project(project_id: int, project: ProjectUpdate):
    connection = sqlite3.connect("september/week2/portfolio.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE projects
        SET project_name = ?, status = ?, cost = ?, delay_days = ?
        WHERE project_id = ?
        """,
        (
            project.project_name,
            project.status,
            project.cost,
            project.delay_days,
            project_id
        )
    )

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    connection.commit()

    connection.close()

    return {
        "message": "Project updated successfully",
        "project_id": project_id
    }

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    connection = sqlite3.connect("september/week2/portfolio.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM projects WHERE project_id = ?",
        (project_id,)
    )

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    connection.commit()
    connection.close()

    return {
        "message": "Project deleted successfully",
        "project_id": project_id
    }