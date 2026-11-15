
from pathlib import Path
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from november.week2.tool_schemas import project_tools
from november.week2.tool_executor import execute_tool


def parse_tool_calls(response):
    """
    Extract function names, arguments and IDs
    from Gemini's response object.
    """

    parsed_calls = []

    if not response.function_calls:
        return parsed_calls

    for function_call in response.function_calls:

        parsed_call = {
            "function_name": function_call.name,
            "arguments": function_call.args,
            "id": function_call.id
        }

        parsed_calls.append(parsed_call)

    return parsed_calls


# Load API key
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Original user question
user_prompt = "Prepare a management review of project 3."


# Send the first request to Gemini
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=user_prompt,
    config=types.GenerateContentConfig(
        tools=[project_tools],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        )
    )
)


# Parse Gemini's response
parsed_calls = parse_tool_calls(response)

print("\nPARSED TOOL CALLS")

for call in parsed_calls:
    print(call)


# Execute requested Python tools
tool_results = []

for call in parsed_calls:

    try:
        result = execute_tool(
            call["function_name"],
            call["arguments"]
        )

    except Exception as error:
        result = {
            "success": False,
            "error": "Unexpected tool execution failure",
            "details": str(error)
        }

    tool_results.append({
        "function_name": call["function_name"],
        "id": call["id"],
        "result": result
    })


print("\nEXECUTION RESULTS")

for item in tool_results:
    print(item)


# Convert Python results into Gemini function responses
function_response_parts = []

for item in tool_results:

    function_response_part = types.Part.from_function_response(
        name=item["function_name"],
        response={
            "result": item["result"]
        }
    )

    function_response_parts.append(function_response_part)


# Prepare the conversation history
conversation_history = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_text(text=user_prompt)
        ]
    ),

    # Preserve Gemini's original function-call response
    response.candidates[0].content,

    # Send Python's execution results back to Gemini
    types.Content(
        role="user",
        parts=function_response_parts
    )
]


# Ask Gemini to generate the final answer
final_response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=conversation_history,
    config=types.GenerateContentConfig(
        tools=[project_tools]
    )
)


print("\nFINAL GEMINI RESPONSE")
print(final_response.text)


