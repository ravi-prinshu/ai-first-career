# October Week 1 — FastAPI & API Fundamentals

## Objective

Learn the fundamentals of building a Python API using FastAPI and connecting it to a SQLite database.

The main application flow learned this week was:

Client → HTTP Request → FastAPI → Python → SQLite → JSON Response

---

## What I Learned

### 1. FastAPI

Created a FastAPI application and built HTTP endpoints.

Example:

GET `/hello`

```json
{
  "message": "Hello Ravi"
}

2. Path Parameters
Used path parameters to retrieve a specific project.
GET /projects/{project_id}

Example:
GET /projects/3

Returns the project with ID 3.
3. Query Parameters
Used query parameters to filter projects.
GET /projects?status=Delayed

This returns projects whose status is Delayed.
4. HTTP Status Codes
Implemented error handling for projects that do not exist.
200 → Successful request
404 → Project not found
500 → Unexpected server error

5. SQLite Integration
Connected FastAPI to the SQLite database created during September Week 2.
Database:
september/week2/portfolio.db

Table:
projects

Columns:
project_id
project_name
status
cost
delay_days

6. GET from Database
The API retrieves project data from SQLite and converts the database records into JSON responses.
7. POST Requests
Created a new project using:
POST /projects

Request body:
{
  "project_name": "Data Platform",
  "status": "On Track",
  "cost": 1800000,
  "delay_days": 0
}

The database generated:
project_id = 6

8. Pydantic Validation
Used a Pydantic model to validate incoming project data.
class ProjectCreate(BaseModel):    project_name: str    status: str    cost: int    delay_days: int


9. Database Insert
Used a parameterized SQL query:
INSERT INTO projects
(project_name, status, cost, delay_days)
VALUES (?, ?, ?, ?)

Used:
connection.commit()


to save the change and:
cursor.lastrowid


to retrieve the generated project ID.
API Endpoints
Method	Endpoint	Purpose
GET	/hello	Test the API
GET	/about	Return learner information
GET	/projects	Retrieve all projects
GET	/projects?status=Delayed	Filter projects by status
GET	/projects/{project_id}	Retrieve one project
POST	/projects	Create a new project


Interactive API documentation is available through FastAPI's /docs endpoint.
Architecture
Client
   ↓
HTTP Request
   ↓
FastAPI Endpoint
   ↓
Python Logic
   ↓
SQLite Database
   ↓
Python Result
   ↓
JSON Response
   ↓
Client

Business/BA Perspective
This week helped connect API concepts with application and business requirements.
Examples:
- "Get project 3" → path parameter
- "Get delayed projects" → query parameter
- "Create a new project" → POST + request body
- "Project does not exist" → 404 response
The focus was not only on writing Python code, but understanding how a business requirement translates into an API design.
Week 1 Outcome
By the end of Week 1, I can:
- Build a basic FastAPI application
- Create GET and POST endpoints
- Use path and query parameters
- Validate request bodies with Pydantic
- Connect an API to SQLite
- Retrieve data from a database
- Insert data into a database
- Handle basic API errors
- Return database data as JSON
- Understand the flow from HTTP request to database and back