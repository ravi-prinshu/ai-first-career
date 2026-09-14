import sqlite3

def get_portfolio_overview(cursor):
    """
    Calculate key portfolio-level metrics.
    """

    # Total number of projects
    cursor.execute("""
    SELECT COUNT(*)
    FROM projects
    """)

    total_projects = cursor.fetchone()[0]


    # Total portfolio cost
    cursor.execute("""
    SELECT SUM(cost)
    FROM projects
    """)

    total_cost = cursor.fetchone()[0]


    # Number of delayed projects
    cursor.execute("""
    SELECT COUNT(*)
    FROM projects
    WHERE status = 'Delayed'
    """)

    delayed_projects = cursor.fetchone()[0]


    # Average delay among delayed projects
    cursor.execute("""
    SELECT AVG(delay_days)
    FROM projects
    WHERE status = 'Delayed'
    """)

    average_delay = cursor.fetchone()[0]


    return total_projects, total_cost, delayed_projects, average_delay

def get_cost_risk_analysis(cursor):
    """
    Calculate cost and risk metrics for the portfolio.
    """

    # Number of high-cost projects
    cursor.execute("""
    SELECT COUNT(*)
    FROM projects
    WHERE cost > 1000000
    """)

    high_cost_projects = cursor.fetchone()[0]


    # Total cost of delayed projects
    cursor.execute("""
    SELECT SUM(cost)
    FROM projects
    WHERE status = 'Delayed'
    """)

    delayed_project_cost = cursor.fetchone()[0]


    # Number of high-risk projects
    # High-risk = Delayed AND cost > ₹10 lakh
    cursor.execute("""
    SELECT COUNT(*)
    FROM projects
    WHERE status = 'Delayed'
    AND cost > 1000000
    """)

    high_risk_projects = cursor.fetchone()[0]


    return high_cost_projects, delayed_project_cost, high_risk_projects

def get_status_breakdown(cursor):
    """
    Calculate project count and total cost for each status.
    """

    cursor.execute("""
    SELECT status,
           COUNT(*) AS number_of_projects,
           SUM(cost) AS total_cost
    FROM projects
    GROUP BY status
    ORDER BY total_cost DESC
    """)

    return cursor.fetchall()

def get_high_risk_projects(cursor):
    """
    Identify projects that are both delayed and high-cost.
    """

    cursor.execute("""
    SELECT project_name,
           cost,
           status
    FROM projects
    WHERE status = 'Delayed'
    AND cost > 1000000
    ORDER BY cost DESC
    """)

    return cursor.fetchall()

def format_currency(amount):
    """
    Format currency for portfolio reporting.
    """
    return f"₹{amount:,}"

def main():

    connection = sqlite3.connect("portfolio.db")

    cursor = connection.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY,
        project_name TEXT,
        status TEXT,
        cost INTEGER,
        delay_days INTEGER
    )
    """)

    connection.commit()
    
    # ========================================================
    # 1. PORTFOLIO OVERVIEW
    # ========================================================

    total_projects, total_cost, delayed_projects, average_delay = \
        get_portfolio_overview(cursor)

    print("\n===== PORTFOLIO OVERVIEW =====")

    print("Total Projects:", total_projects)
    print("Total Portfolio Cost:", format_currency(total_cost))
    print("Delayed Projects:", delayed_projects)
    print("Average Delay:", round(average_delay, 2), "days")


    # ========================================================
    # 2. COST & RISK ANALYSIS
    # ========================================================

    high_cost_projects, delayed_project_cost, high_risk_projects = \
        get_cost_risk_analysis(cursor)

    print("\n===== COST & RISK ANALYSIS =====")

    print("High-Cost Projects:", high_cost_projects)
    print("Total Cost of Delayed Projects: ₹", format_currency(delayed_project_cost))
    print("High-Risk Projects:", high_risk_projects)


    # ========================================================
    # 3. STATUS BREAKDOWN
    # ========================================================

    status_breakdown = get_status_breakdown(cursor)

    print("\n===== STATUS BREAKDOWN =====")

    for status, number_of_projects, total_cost in status_breakdown:
        print(
            status,
            "| Projects:", number_of_projects,
            "| Total Cost: ", format_currency(total_cost)
        )


    # ========================================================
    # 4. HIGH-RISK PROJECTS
    # ========================================================

    high_risk_project_details = get_high_risk_projects(cursor)

    print("\n===== HIGH-RISK PROJECTS =====")

    for project_name, cost, status in high_risk_project_details:
        print(
            project_name,
            "| ", format_currency(cost),
            "|", status
        )


    # ============================================================
    # 5. JOIN PRACTICE
    # ============================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_managers (
            project_id INTEGER PRIMARY KEY,
            manager_name TEXT
        )
        """)

    connection.commit()

    # Insert project data
    projects = [
            (1, "ERP", "Delayed", 1200000, 45),
            (2, "CRM", "On Track", 800000, 0),
            (3, "Data Migration", "Delayed", 1500000, 60),
            (4, "Mobile App", "On Track", 600000, 10),
            (5, "Cloud Migration", "Delayed", 2000000, 35)
        ]

    cursor.executemany("""
        INSERT OR IGNORE INTO projects
        (project_id, project_name, status, cost, delay_days)
        VALUES (?, ?, ?, ?, ?)
        """, projects)

    connection.commit()

    managers = [
        (1, "Amit"),
        (2, "Priya"),
        (3, "Rahul"),
        (4, "Sneha")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO project_managers
        (project_id, manager_name)
        VALUES (?, ?)
        """, managers)

    connection.commit()

    # ============================================================
    # INNER JOIN
    # ============================================================

    cursor.execute("""
    SELECT p.project_name,
        pm.manager_name
    FROM projects p
    LEFT JOIN project_managers pm
        ON p.project_id = pm.project_id
    """)

    joined_projects = cursor.fetchall()

    print("\n===== PROJECT MANAGERS — LEFT JOIN =====")

    for project_name, manager_name in joined_projects:
        print(project_name, "| Manager:", manager_name)

    cursor.execute("""
    SELECT p.project_name
    FROM projects p
    LEFT JOIN project_managers pm
        ON p.project_id = pm.project_id
    WHERE pm.manager_name IS NULL
    """)

    unassigned_projects = cursor.fetchall()

    print("\n===== PROJECTS WITHOUT MANAGERS =====")

    for project in unassigned_projects:
        print(project[0])

    connection.close()

# ============================================================
# PROGRAM ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()