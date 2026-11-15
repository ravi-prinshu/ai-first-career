from pathlib import Path
import sqlite3


# Locate the existing project database
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "september" / "week2" / "portfolio.db"


def get_project_details(project_id: int) -> dict:
    """
    Retrieve project details using the project ID.

    Args:
        project_id: Unique identifier of the project.

    Returns:
        Dictionary containing project details or an error.
    """

    # Validate input
    if isinstance(project_id, bool) or not isinstance(project_id, int):
        return {
            "success": False,
            "error": "Project ID must be an integer."
        }

    if project_id <= 0:
        return {
            "success": False,
            "error": "Project ID must be greater than zero."
        }

    if not DB_PATH.is_file():
        return {
            "success": False,
            "error": "Project database not found."
        }

    connection = None

    try:
        # Connect to SQLite
        connection = sqlite3.connect(DB_PATH)

        # Return database records as dictionary-like rows
        connection.row_factory = sqlite3.Row

        # Retrieve project
        cursor = connection.execute(
            """
            SELECT project_id, project_name, status, cost, delay_days
            FROM projects
            WHERE project_id = ?
            """,
            (project_id,)
        )

        project = cursor.fetchone()

        # Handle missing project
        if project is None:
            return {
                "success": False,
                "error": f"Project ID {project_id} not found."
            }

        # Return structured result
        return {
            "success": True,
            "project": dict(project)
        }

    except sqlite3.Error:
        return {
            "success": False,
            "error": "Database operation failed."
        }

    finally:
        if connection is not None:
            connection.close()


def list_projects(status: str = None) -> dict:
    """
    Retrieve all projects or filter projects by status.

    Args:
        status: Optional project status filter.

    Returns:
        Dictionary containing matching project records.
    """

    if status is not None:
        if not isinstance(status, str):
            return {
                "success": False,
                "error": "Status must be a string."
            }

        status = status.strip()

        if not status:
            return {
                "success": False,
                "error": "Status cannot be empty."
            }

        if status not in ["Delayed", "On Track"]:
            return {
                "success": False,
                "error": "Invalid status. Use Delayed or On Track."
            }

    connection = None

    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row

        if status is None:
            cursor = connection.execute(
                """
                SELECT project_id, project_name, status, cost, delay_days
                FROM projects
                """
            )
        else:
            cursor = connection.execute(
                """
                SELECT project_id, project_name, status, cost, delay_days
                FROM projects
                WHERE status = ?
                """,
                (status,)
            )

        projects = [dict(row) for row in cursor.fetchall()]

        return {
            "success": True,
            "count": len(projects),
            "projects": projects
        }

    except sqlite3.Error:
        return {
            "success": False,
            "error": "Database operation failed."
        }

    finally:
        if connection is not None:
            connection.close()

def calculate_project_risk(project_id: int) -> dict:
    """
    Calculate project risk using cost and delay.

    Args:
        project_id: Unique identifier of the project.

    Returns:
        Dictionary containing project details and calculated risk.
    """

    # Step 1: Retrieve project details using the existing function
    result = get_project_details(project_id)

    # Step 2: Handle errors returned by get_project_details()
    if not result["success"]:
        return result

    # Step 3: Extract project information
    project = result["project"]

    cost = project["cost"]
    delay_days = project["delay_days"]

    # Step 4: Apply the agreed business rules
    if delay_days == 0:
        risk_level = "Low"

    elif delay_days > 0 and cost > 1000000:
        risk_level = "High"

    else:
        risk_level = "Medium"

    # Step 5: Return the result in a predictable structure
    return {
        "success": True,
        "project_id": project["project_id"],
        "project_name": project["project_name"],
        "cost": cost,
        "delay_days": delay_days,
        "risk_level": risk_level
    }


# Test the function independently
if __name__ == "__main__":

    print("HIGH RISK")
    print(calculate_project_risk(1))

    print("\nMEDIUM RISK")
    print(calculate_project_risk(4))

    print("\nLOW RISK")
    print(calculate_project_risk(2))

    print("\nMISSING PROJECT")
    print(calculate_project_risk(999))

    print("\nINVALID PROJECT ID")
    print(calculate_project_risk("3"))