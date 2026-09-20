import sqlite3
import json
from enum import Enum

from google import genai
from pydantic import BaseModel


DB_PATH = "../week2/portfolio.db"


# -----------------------------
# Risk Models
# -----------------------------

class RiskLevel(str, Enum):
    HIGH = "High Risk"
    MEDIUM = "Medium Risk"
    LOW = "Low Risk"


class RiskAssessment(BaseModel):
    project_name: str
    risk_level: RiskLevel
    reason: str
    recommended_actions: list[str]


class RiskAssessmentBatch(BaseModel):
    assessments: list[RiskAssessment]


# -----------------------------
# Gemini Client
# -----------------------------

client = genai.Client()


# -----------------------------
# Get Projects from Database
# -----------------------------

def get_projects():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT project_name, status, cost, delay_days
        FROM projects
    """)

    projects = cursor.fetchall()

    connection.close()

    return projects


# -----------------------------
# Convert Database Rows
# -----------------------------

def get_project_details():

    projects = get_projects()

    projects_details = []

    for project in projects:

        project_detail = {
            "project_name": project[0],
            "status": project[1],
            "cost": project[2],
            "delay_days": project[3]
        }

        projects_details.append(project_detail)

    return projects_details


# -----------------------------
# Create ONE Prompt
# -----------------------------

def create_risk_prompt(projects):

    project_information = ""

    for project in projects:

        project_information += f"""
Project Name: {project["project_name"]}
Status: {project["status"]}
Cost: ₹{project["cost"]:,}
Delay: {project["delay_days"]} days

"""

    prompt = f"""
You are a Project Risk Analyst.

Analyze ALL of the following projects.

{project_information}

Business rules:

1. A project is considered delayed if delay_days is greater than 0.
2. A project is High Risk if its cost is above ₹10 lakh AND it is delayed.
3. A project is Medium Risk if it is delayed but its cost is ₹10 lakh or less.
4. A project is Low Risk if it has no delay.

For each project:

- Determine the risk level.
- Explain the reason for the assigned risk level.
- Recommend practical actions that a project manager could take.

Analyze every project provided.

Return one risk assessment for each project according to the provided structured output schema.
"""

    return prompt


# -----------------------------
# Analyze ALL Projects
# ONE API CALL
# -----------------------------

def analyze_all_projects(projects):

    prompt = create_risk_prompt(projects)

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": RiskAssessmentBatch.model_json_schema()
        },
    )

    result = RiskAssessmentBatch.model_validate_json(
        interaction.output_text
    )

    return result


# -----------------------------
# Expected Risk
# -----------------------------

def expected_risk(project):

    if project["delay_days"] > 0:

        if project["cost"] > 1000000:
            return "High Risk"

        return "Medium Risk"

    return "Low Risk"


# -----------------------------
# Evaluate AI Results
# -----------------------------

def evaluate_results(projects, ai_results):

    project_lookup = {
        project["project_name"]: project
        for project in projects
    }

    correct = 0

    print("\n")
    print("=" * 60)
    print("EVALUATION")
    print("=" * 60)

    for result in ai_results:

        project = project_lookup[result.project_name]

        expected = expected_risk(project)
        actual = result.risk_level.value

        if expected == actual:
            status = "PASS"
            correct += 1
        else:
            status = "FAIL"

        print(
            f"{result.project_name}: "
            f"Expected={expected}, "
            f"AI={actual}, "
            f"Result={status}"
        )

    accuracy = (correct / len(projects)) * 100

    print("\nAccuracy:", f"{accuracy:.2f}%")

    return accuracy


# -----------------------------
# Save and Display AI Results
# -----------------------------

def save_results(results):

    with open("risk_results.json", "w", encoding="utf-8") as file:
        json.dump(
            [risk.model_dump() for risk in results],
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nResults saved to risk_results.json")

def display_results(results):

    print("\n")
    print("=" * 60)
    print("AI PROJECT RISK ANALYZER")
    print("=" * 60)

    for risk in results:

        print(f"\nProject: {risk.project_name}")
        print(f"Risk Level: {risk.risk_level.value}")
        print(f"Reason: {risk.reason}")

        print("Recommended Actions:")

        for action in risk.recommended_actions:
            print(f"- {action}")


# -----------------------------
# Main
# -----------------------------

def main():

    projects = get_project_details()

    print(f"Projects found: {len(projects)}")

    print("\nSending ONE request to Gemini...")
    
    result = analyze_all_projects(projects)

    save_results(result.assessments)

    display_results(result.assessments)

    evaluate_results(
        projects,
        result.assessments
    )


if __name__ == "__main__":
    main()