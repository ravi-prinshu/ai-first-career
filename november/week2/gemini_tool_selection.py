
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .tool_schemas import project_tools


# Step 1: Locate the repository root and load the API key
PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Step 2: Create the Gemini client
client = genai.Client(api_key=api_key)


# Step 3: Send a request to Gemini with our tool schemas
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Give me the complete details of project 3",
    config=types.GenerateContentConfig(
        tools=[project_tools],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        )
    )
)


# Step 4: Inspect Gemini's response
print("\nGEMINI RESPONSE")

if response.function_calls:
    for function_call in response.function_calls:
        print("Selected tool:", function_call.name)
        print("Arguments:", function_call.args)
else:
    print("Gemini did not request a tool.")
    print("Response:", response.text)
