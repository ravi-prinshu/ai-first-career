
import json

from .tools import (
    get_project_details,
    list_projects,
    calculate_project_risk
)


# Step 1: Create an allowlist mapping Gemini tool names
# to their corresponding Python functions.

available_functions = {
    "get_project_details": get_project_details,
    "list_projects": list_projects,
    "calculate_project_risk": calculate_project_risk
}


# Step 2: Create a function to execute Gemini tool requests.

def execute_tool(function_name: str, arguments: dict) -> dict:
    """
    Identify and execute an approved Python tool.

    Args:
        function_name: Name of the function requested by Gemini.
        arguments: Arguments supplied by Gemini.

    Returns:
        Dictionary containing the function result or an error.
    """

    # Check whether the requested tool is registered.
    if function_name not in available_functions:
        return {
            "success": False,
            "error": f"Unknown tool: {function_name}"
        }

    # Validate the arguments structure.
    if not isinstance(arguments, dict):
        return {
            "success": False,
            "error": "Tool arguments must be a dictionary."
        }

    # Retrieve the approved Python function.
    selected_function = available_functions[function_name]

    # Execute the function safely.
    try:
        result = selected_function(**arguments)

        return result

    except TypeError:
        return {
            "success": False,
            "error": "Invalid arguments supplied to the tool."
        }

    except Exception:
        return {
            "success": False,
            "error": "An unexpected error occurred during tool execution."
        }


# Step 3: Test the executor independently.

if __name__ == "__main__":

    print("VALID TOOL REQUEST")
    print(
        execute_tool(
            "calculate_project_risk",
            {"project_id": 3}
        )
    )

    print("\nSECOND VALID TOOL REQUEST")
    print(
        execute_tool(
            "list_projects",
            {"status": "Delayed"}
        )
    )

    print("\nINVALID TOOL REQUEST")
    print(
        execute_tool(
            "delete_all_projects",
            {}
        )
    )

    print("\nINVALID ARGUMENT")
    print(
        execute_tool(
            "calculate_project_risk",
            {"project_id": "abc"}
        )
    )
