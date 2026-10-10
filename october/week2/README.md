# October Week 2 — Database CRUD with FastAPI

## Objective

Extend the Week 1 FastAPI application to support all four CRUD operations through HTTP endpoints connected to SQLite.

CRUD stands for:

- **Create** — add a new project
- **Read** — retrieve project information
- **Update** — modify an existing project
- **Delete** — remove a project

## Architecture

Client → HTTP Request → FastAPI → Python Logic → SQLite → JSON Response

## What I Learned

### 1. Create — POST

Endpoint: `POST /projects`

- Receive project details in the request body.
- Validate input using a Pydantic model.
- Insert the record into SQLite using a parameterized SQL query.
- Use `connection.commit()` to save the change.
- Use `cursor.lastrowid` to retrieve the generated project ID.

### 2. Read — GET

Endpoints:

- `GET /projects` — retrieve all projects.
- `GET /projects/{project_id}` — retrieve one project.
- `GET /projects?status=Delayed` — filter projects by status.

Used SQL `SELECT`, path parameters, query parameters, and JSON responses.

### 3. Update — PUT

Endpoint: `PUT /projects/{project_id}`

- Receive the project ID through the path.
- Validate the complete project representation using Pydantic.
- Execute SQL `UPDATE` with parameterized values.
- Use `connection.commit()` to persist the update.
- Use `cursor.rowcount` to detect when no record was updated.
- Return HTTP 404 when the requested project does not exist.

### 4. Delete — DELETE

Endpoint: `DELETE /projects/{project_id}`

- Delete the requested record using SQL `DELETE`.
- Use the project ID to target the intended record.
- Check `cursor.rowcount` to detect nonexistent projects.
- Commit successful deletions.
- Return HTTP 404 when the requested project does not exist.

### 5. Error Handling

Learned to return appropriate HTTP responses rather than reporting success when an operation fails.

- `200` — successful operation
- `404` — requested project not found
- `422` — request validation error from FastAPI/Pydantic

### 6. Parameterized SQL

Used `?` placeholders to pass values separately from SQL statements.

Parameterized queries help prevent SQL injection and keep query structure separate from input values.

### 7. Database Transactions

Used `connection.commit()` to persist successful changes to SQLite.

Verified updates and deletions by making subsequent GET requests.

## API Endpoint Summary

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/projects` | Retrieve all projects |
| GET | `/projects/{project_id}` | Retrieve one project |
| GET | `/projects?status=Delayed` | Filter by status |
| POST | `/projects` | Create a project |
| PUT | `/projects/{project_id}` | Update a project |
| DELETE | `/projects/{project_id}` | Delete a project |

## Business Analysis Perspective

This week connected business requirements with API behavior:

- Retrieve a project → GET by ID
- Filter delayed projects → GET with a query parameter
- Create a project → POST with a request body
- Update project information → PUT
- Delete a project → DELETE
- Request a nonexistent project → HTTP 404

The focus was understanding the interaction between the API layer, Python application logic, and database.

## Outcome

By the end of Week 2, I extended the application to support CRUD operations, request validation, parameterized SQL, database persistence, and basic error handling.

## Next

October Week 3 — Integrate an LLM into the API application.