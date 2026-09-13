# September Week 1 — Project Data Processor
## n Project Objective
Build a Python program that processes project data stored in a JSON file and generates a summary report based on d
The project simulates a simple **project portfolio analysis** use case that could be relevant for a Business Analy
---
## n Input
The program reads project information from:
`projects.json`
Each project contains:
- Project name
- Project status
- Project cost
- Delay days
Example:
```json
{
"name": "ERP",
"status": "Delayed",
"cost": 1200000,
"delay_days": 45
}
```
---
## nn Business Requirements
The program performs the following analysis:
1. Count the number of delayed projects.
2. Calculate the total cost of all projects.
3. Calculate the average delay among delayed projects.
4. Identify projects costing more than n10 lakh.
5. Identify high-risk projects.
6. Generate a summary report.
7. Save the summary as a JSON file.
### High-Risk Definition
A project is considered **High Risk** when:
- Status = `Delayed`
- AND
- Cost > `1,000,000`
---
## n Functions Created
### `count_delayed_projects(projects)`
Counts the number of projects whose status is `Delayed`.
### `calculate_total_cost(projects)`
Calculates the total cost of all projects.
### `calculate_average_delay(projects, decimal_places=2)`
Calculates the average delay only among delayed projects.
The function also handles the case where there are no delayed projects.
### `get_high_cost_projects(projects)`
Returns the names of projects whose cost is greater than n1,000,000.
### `get_high_risk_projects(projects)`
Returns the names of projects that are both:
- Delayed
- High Cost
### `main()`
Controls the overall program flow:
1. Load project data.
2. Process the data.
3. Generate the summary.
4. Save the summary.
5. Read the generated report.
6. Display the report.
---
## nn Error Handling
The program handles two common input-file errors.
### Missing File
If `projects.json` does not exist:
```text
Error: projects.json was not found.
```
### Invalid JSON
If `projects.json` contains invalid JSON:
```text
Error: projects.json contains invalid JSON.
```
This prevents the program from crashing with an unhelpful raw error message.
---
## n Expected Analysis
For the current project dataset:
| Metric | Result |
|---|---:|
| Total Projects | 5 |
| Delayed Projects | 3 |
| Total Project Cost | n61,00,000 |
| Average Delay | 46.67 days |
| High-Cost Projects | 3 |
| High-Risk Projects | 3 |
### High-Cost Projects
- ERP
- Data Migration
- Cloud Migration
### High-Risk Projects
- ERP
- Data Migration
- Cloud Migration
---
## n Output
The program generates:
`project_summary.json`
The output contains the calculated project portfolio summary.
Example structure:
```json
{
"delayed_projects": 3,
"total_cost": 6100000,
"average_delay": 46.67,
"high_cost_projects": [
"ERP",
"Data Migration",
"Cloud Migration"
],
"high_risk_projects": [
"ERP",
"Data Migration",
"Cloud Migration"
]
}
```
---
## nn How to Run
Open the VS Code terminal and navigate to the project folder:
```powershell
cd .\september\week1\
```
Activate the virtual environment:
```powershell
.\.venv\Scripts\Activate.ps1
```
Run the Python program:
```powershell
python project_data_processor.py
```
---
## n Python Concepts Practiced
This project combines several Python concepts learned during August and September Week 1:
- Variables
- Data types
- Lists
- Dictionaries
- List of dictionaries
- `for` loops
- `if` conditions
- Boolean operators
- Functions
- Parameters and arguments
- `return`
- List comprehensions
- JSON
- Reading files
- Writing files
- Exception handling
- `try / except`
- `FileNotFoundError`
- `JSONDecodeError`
- `round()`
- Default function parameters
- `main()` function
- `if __name__ == "__main__":`
---
## n Business / BA-PM Learning
This project demonstrates how Python can be used to convert raw project data into useful management information.
The same approach can be extended to real-world use cases such as:
- Project portfolio reporting
- PMO dashboards
- Risk analysis
- Budget tracking
- Delivery governance
- Delay analysis
- Management reporting
- Portfolio prioritization
The important learning is not just writing Python code, but using code to answer **business questions from structu
---
## n Project Structure
```text
september/
nnn week1/
nnn README.md
nnn projects.json
nnn project_data_processor.py
nnn project_summary.json
```
---
## n Status
**September Week 1 — Completed**
Next:
**September Week 2 — SQL & Data Analysis**