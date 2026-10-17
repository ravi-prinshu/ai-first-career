import os
import sqlite3
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI, HTTPException
from google.genai.errors import APIError

class AIProjectAssessment(BaseModel):
    key_concerns: list[str]
    recommended_actions: list[str]

app = FastAPI()

project_root = Path(__file__).resolve().parents[2]
load_dotenv(project_root / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)

def get_project_from_db(project_id: int):
    connection = sqlite3.connect(
        project_root / "september" / "week2" / "portfolio.db"
    )
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT project_id, project_name, status, cost, delay_days
        FROM projects
        WHERE project_id = ?
        """,
        (project_id,)
    )

    project = cursor.fetchone()
    connection.close()

    return project

def calculate_project_risk(cost: int, delay_days: int) -> str:
    if delay_days == 0:
        return "Low"

    if cost > 1_000_000:
        return "High"

    return "Medium"

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
    cost=project_data["cost"],
    delay_days=project_data["delay_days"]
    )   

    try:
        response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
        You are a business project risk analyst.

        Analyse this project using only the supplied data.

        Project data:
        {project_data}

        Identify the main concerns and recommend practical actions.
        Do not invent missing project facts.
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": AIProjectAssessment,
        },
        )

        assessment = AIProjectAssessment.model_validate_json(response.text)
    except APIError:
        raise HTTPException(
            status_code=502,
            detail="The AI service is currently unavailable. Please try again later."
        )

    return {
    "project": project_data,
    "rule_based_risk": rule_based_risk,
    "assessment": assessment.model_dump()
    }

@app.get("/ask-ai")
def ask_ai(question: str):
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

    return {
        "question": question,
        "answer": response.text
    }