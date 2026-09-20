from google import genai
from pydantic import BaseModel
from enum import Enum


class RiskLevel(str, Enum):
    HIGH = "High Risk"
    MEDIUM = "Medium Risk"
    LOW = "Low Risk"


class RiskAssessment(BaseModel):
    project_name: str
    risk_level: RiskLevel
    reason: str
    recommended_actions: list[str]


client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="""
You are a Project Risk Analyst.

Analyze the following project:

Project Name: ERP Implementation
Status: Delayed
Cost: ₹12,00,000
Delay: 45 days

Business rule:
A project is High Risk if its cost is above ₹10 lakh AND it is delayed.

Determine the risk level, explain the reason, and recommend appropriate actions.
""",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": RiskAssessment.model_json_schema()
    },
)

risk = RiskAssessment.model_validate_json(interaction.output_text)

print(risk.project_name)
print(risk.risk_level.value)
print(risk.reason)