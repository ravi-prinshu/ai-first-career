Project Overview
This project demonstrates how Python and SQL can be used together to analyze a project portfolio stored in a
SQLite database. The goal is to convert raw project data into useful portfolio-level insights that can support project
and management decision-making.
Business Objective
Analyze a portfolio of projects and identify: overall portfolio size and cost; delayed projects; average delay;
high-cost projects; financial exposure from delayed projects; high-risk projects; and project status breakdown.
Project Structure
week2/
nnn portfolio_analysis.py
nnn portfolio.db
nnn README.md
Database Structure
Column Type Description
project_id INTEGER Unique project identifier
project_name TEXT Name of the project
status TEXT Project status
cost INTEGER Project cost
delay_days INTEGER Number of delay days
Project Data
Project Status Cost Delay
ERP Delayed n12,00,000 45 days
CRM On Track n8,00,000 0 days
Data Migration Delayed n15,00,000 60 days
Mobile App On Track n6,00,000 10 days
Cloud Migration Delayed n20,00,000 35 days
Business Questions Answered
1. Portfolio Overview
• Total number of projects
• Total portfolio cost
• Number of delayed projects
• Average delay among delayed projects
Results: Total Projects: 5; Total Portfolio Cost: n61,00,000; Delayed Projects: 3; Average Delay: 46.67 days.
2. Cost &amp; Risk Analysis
• Number of high-cost projects
• Total cost of delayed projects
• Number of high-risk projects
Business Rules
High-cost project
Cost > n10,00,000
High-risk project
Status = Delayed
AND
Cost > n10,00,000
Results: High-Cost Projects: 3; Total Cost of Delayed Projects: n47,00,000; High-Risk Projects: 3.
3. Status Breakdown
Status Projects Total Cost
Delayed 3 n47,00,000
On Track 2 n14,00,000
4. High-Risk Projects
Project Cost Status
Cloud Migration n20,00,000 Delayed
Data Migration n15,00,000 Delayed
ERP n12,00,000 Delayed
These projects are sorted by cost in descending order to help prioritize projects with greater financial exposure.
SQL Concepts Practiced
SELECT • WHERE • AND / OR • ORDER BY • COUNT(), SUM(), AVG() • GROUP BY • HAVING • JOIN •
Subqueries
Example subquery:
SELECT project_name
FROM projects
WHERE cost > (SELECT AVG(cost) FROM projects);
Python Concepts Practiced
SQLite with Python • sqlite3 • Database connections • Cursors • execute() • executemany() • fetchone() • fetchall()
• Functions • Function parameters • return • for loops • Tuples • String formatting • main() • if __name__ ==
"__main__"
Python + SQL Flow
Python
↓
SQLite Database
↓
SQL Query
↓
Query Result
↓
Python Processing
↓
Management-Friendly Output
Key Learning
SQL is used to retrieve, filter, aggregate, group, and analyze project data. Python is used to connect to the
database, execute SQL, process query results, organize the application using functions, and present the analysis
clearly.
How to Run
python portfolio_analysis.py
The program will create/connect to the SQLite database, load the project data, perform the analysis, and display
the portfolio report.
Example Output
===== PORTFOLIO OVERVIEW =====
Total Projects: 5
Total Portfolio Cost: n6,100,000
Delayed Projects: 3
Average Delay: 46.67 days
===== COST & RISK ANALYSIS =====
High-Cost Projects: 3
Total Cost of Delayed Projects: n4,700,000
High-Risk Projects: 3
===== STATUS BREAKDOWN =====
Delayed | Projects: 3 | Total Cost: n4,700,000
On Track | Projects: 2 | Total Cost: n1,400,000
===== HIGH-RISK PROJECTS =====
Cloud Migration | n2,000,000 | Delayed
Data Migration | n1,500,000 | Delayed
ERP | n1,200,000 | Delayed
Project Outcome
This project demonstrates the ability to combine SQL and Python to transform project-level data into actionable
portfolio insights. The analysis can help project and program managers understand portfolio health, schedule risk,
financial exposure, high-priority projects, and overall project status.