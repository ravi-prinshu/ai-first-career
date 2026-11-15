
from google.genai import types


get_project_details_schema = {
    "name": "get_project_details",
    "description": (
        "Retrieve detailed information about a specific project "
        "using its unique project ID. Use this when the user asks "
        "for details about an individual project."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "project_id": {
                "type": "INTEGER",
                "description": "The unique ID of the project."
            }
        },
        "required": ["project_id"]
    }
}


list_projects_schema = {
    "name": "list_projects",
    "description": (
        "Retrieve all projects when no status is provided, "
        "or filter projects by status when a status is specified. "
        "Use this for requests involving project lists or project status."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "status": {
                "type": "STRING",
                "description": (
                    "Optional project status filter. "
                    "Allowed values are Delayed or On Track."
                )
            }
        },
        "required": []
    }
}


calculate_project_risk_schema = {
    "name": "calculate_project_risk",
    "description": (
        "Calculate the risk level of a specific project using its "
        "cost and delay days. Risk is High when a delayed project "
        "costs more than 1000000, Medium when it is delayed and "
        "costs 1000000 or less, and Low when delay days are zero."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "project_id": {
                "type": "INTEGER",
                "description": "The unique ID of the project."
            }
        },
        "required": ["project_id"]
    }
}


# Register the three function declarations as Gemini tools
project_tools = types.Tool(
    function_declarations=[
        get_project_details_schema,
        list_projects_schema,
        calculate_project_risk_schema
    ]
)


if __name__ == "__main__":
    print("Gemini tool schemas created successfully.")
    print(f"Number of registered tools: {len(project_tools.function_declarations)}")
