
import os
import shutil
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai.errors import APIError
from pydantic import BaseModel, ValidationError

app = FastAPI()

# --------------------------------------------------
# Configuration
# --------------------------------------------------

project_root = Path(__file__).resolve().parents[2]

source_db = project_root / "september" / "week2" / "portfolio.db"
test_db = project_root / "october" / "week4" / "portfolio_test.db"

load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# Database setup
# --------------------------------------------------

def initialize_database():
    """Create a separate Week 4 test database if needed."""

    if not test_db.exists():
        shutil.copy2(source_db, test_db)


initialize_database()


def get_connection():
    return sqlite3.connect(test_db)


def get_project_from_db(project_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT project_id, project_name, status, cost, delay_days
            FROM projects
            WHERE project_id = ?
            """,
            (project_id,)
        )

        return cursor.fetchone()

    finally:
        connection.close()


# --------------------------------------------------
# Request and response models
# --------------------------------------------------

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


class AIProjectAssessment(BaseModel):
    key_concerns: list[str]
    recommended_actions: list[str]


# --------------------------------------------------
# Rule-based risk assessment
# --------------------------------------------------

def calculate_project_risk(
    status: str,
    cost: int,
    delay_days: int
) -> str:

    # On Track status takes priority.
    if status == "On Track":
        return "Low"

    # Delayed projects above ₹10 lakh are High risk.
    if status == "Delayed" and delay_days > 0 and cost > 1_000_000:
        return "High"

    # Other delayed projects are Medium risk.
    return "Medium"

def check_project_consistency(
    status: str,
    delay_days: int
) -> list[str]:
    warnings = []

    if status == "On Track" and delay_days > 0:
        warnings.append(
            f"Project status is On Track despite a recorded "
            f"delay of {delay_days} days. Verify the project status."
        )

    return warnings

# --------------------------------------------------
# Basic endpoints
# --------------------------------------------------

@app.get("/hello")
def hello():
    return {"message": "Hello Ravi"}


@app.get("/about")
def about():
    return {
        "name": "Ravi",
        "role": "AI-First Learner"
    }


# --------------------------------------------------
# Read projects
# --------------------------------------------------

@app.get("/projects")
def get_projects(status: str | None = None):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        if status is None:
            cursor.execute(
                """
                SELECT project_id, project_name, status, cost, delay_days
                FROM projects
                """
            )
        else:
            cursor.execute(
                """
                SELECT project_id, project_name, status, cost, delay_days
                FROM projects
                WHERE status = ?
                """,
                (status,)
            )

        projects = cursor.fetchall()

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

    finally:
        connection.close()


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


# --------------------------------------------------
# Create a project
# --------------------------------------------------

@app.post("/projects")
def create_project(project: ProjectCreate):
    connection = get_connection()

    try:
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

        return {
            "project_id": cursor.lastrowid,
            "project_name": project.project_name,
            "status": project.status,
            "cost": project.cost,
            "delay_days": project.delay_days
        }

    finally:
        connection.close()


# --------------------------------------------------
# Update a project
# --------------------------------------------------

@app.put("/projects/{project_id}")
def update_project(project_id: int, project: ProjectUpdate):
    connection = get_connection()

    try:
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
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        connection.commit()

        return {
            "message": "Project updated successfully",
            "project_id": project_id
        }

    finally:
        connection.close()


# --------------------------------------------------
# Delete a project
# --------------------------------------------------

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM projects WHERE project_id = ?",
            (project_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        connection.commit()

        return {
            "message": "Project deleted successfully",
            "project_id": project_id
        }

    finally:
        connection.close()


# --------------------------------------------------
# AI project analysis
# --------------------------------------------------

@app.get("/projects/{project_id}/analyze")
def analyze_project(project_id: int):
    project = get_project_from_db(project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    project_data = {
        "project_id": project[0],
        "project_name": project[1],
        "status": project[2],
        "cost": project[3],
        "delay_days": project[4]
    }

    rule_based_risk = calculate_project_risk(
        status=project_data["status"],
        cost=project_data["cost"],
        delay_days=project_data["delay_days"]
    )

    consistency_warnings = check_project_consistency(
    status=project_data["status"],
    delay_days=project_data["delay_days"]
    )   

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"""
            You are a business project risk analyst.

            The project cost is denominated in Indian Rupees (INR).
            Always express costs in INR (₹), using Indian number
            formatting where appropriate. Never convert costs to USD.

            Analyse this project using only the supplied data.

            Project data:
            {project_data}

            Rule-based risk:
            {rule_based_risk}

            Data consistency warnings:
            {consistency_warnings}

            Identify the main concerns and recommend practical actions.
            Do not invent missing project facts.
            Keep recommendations concise.
            """,
            config={
                "response_mime_type": "application/json",
                "response_schema": AIProjectAssessment,
            },
        )

        assessment = AIProjectAssessment.model_validate_json(
            response.text
        )

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="The AI service is currently unavailable. Please try again later."
        )

    except (ValidationError, ValueError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="The AI service returned an invalid assessment."
        )

    return {
    "project": project_data,
    "rule_based_risk": rule_based_risk,
    "consistency_warnings": consistency_warnings,
    "assessment": assessment.model_dump()
    }


# --------------------------------------------------
# General AI assistant
# --------------------------------------------------

@app.get("/ask-ai")
def ask_ai(question: str):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"""
            You are a business project management assistant.

            Answer the following question:
            {question}

            Instructions:
            - Use no more than 3 bullet points.
            - Use simple business language.
            - Focus on practical reasons and actions.
            - Avoid unnecessary background information.
            """
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="The AI service returned an empty response."
            )

        return {
            "question": question,
            "answer": response.text
        }

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="The AI service is currently unavailable. Please try again later."
        )
