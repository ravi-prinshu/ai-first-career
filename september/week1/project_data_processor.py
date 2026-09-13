import json

def count_delayed_projects(projects):

    delayed_count = 0

    for project in projects:
        if project["status"] == "Delayed":
            delayed_count += 1

    return delayed_count

def calculate_total_cost(projects):

    total_cost = 0

    for project in projects:
        total_cost += project["cost"]

    return total_cost

def calculate_average_delay(projects, decimal_places=2):

    total_delay = 0
    delayed_count = count_delayed_projects(projects)

    for project in projects:
        if project["status"] == "Delayed":
            total_delay += project["delayed_days"]

    if delayed_count == 0:
        return 0
    
    return round(total_delay / delayed_count, decimal_places)

def get_high_cost_projects(projects):

    high_cost_projects = [
        project["name"]
        for project in projects
        if project["cost"] > 1000000
    ]

    return high_cost_projects

def get_high_risk_projects(projects):

    high_risk_projects = [
        project["name"]
        for project in projects
        if project["cost"] > 1000000 and project["status"] == "Delayed"
    ]

    return high_risk_projects

def main():
    try:
        with open("projects.json", "r") as file:
            projects = json.load(file)

    except FileNotFoundError:
        print("Error: projects.json was not found.")
        return
    
    except json.JSONDecodeError:
        print("Error: projects.json contains invalid JSON.")
        return

    summary={}

    summary["delayed_projects"] = count_delayed_projects(projects)
    summary["total_cost"] = calculate_total_cost(projects)
    summary["average_delay"] = calculate_average_delay(projects)
    summary["high_cost_projects"] = get_high_cost_projects(projects)
    summary["high_risk_projects"] = get_high_risk_projects(projects)

    with open("project_summary.json", "w") as file:
        json.dump(summary, file, indent=4)

    with open("project_summary.json", "r") as file:
        report = json.load(file)

    print(report)

if __name__ == "__main__":
    main()