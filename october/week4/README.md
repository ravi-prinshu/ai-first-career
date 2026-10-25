# October Week 4 — Integrated AI Project Risk Analyzer

## 1. Project Overview

This project integrates a REST API, a SQLite database, Python-based business rules, and Google's Gemini AI into a single application.

The application allows users to manage project records, calculate rule-based project risk, identify inconsistencies in project information, and generate AI-powered risk assessments with practical recommendations.

**Objective:** Demonstrate how APIs, persistent data, deterministic business rules, and generative AI can work together to support project management decisions.

## 2. Technologies Used

- **Python** — Application logic and business rules
- **FastAPI** — REST API development
- **SQLite** — Persistent project data storage
- **Pydantic** — Request validation and structured AI output
- **Google Gemini API** — AI-generated project analysis and recommendations
- **python-dotenv** — Environment variable configuration
- **Uvicorn** — Local application server

## 3. Application Architecture

The application follows this workflow:

1. FastAPI receives a request.
2. SQLite stores or retrieves the project information.
3. Python calculates the rule-based risk.
4. A consistency-check function identifies contradictory project data.
5. Gemini receives the project information, calculated risk, and consistency warnings.
6. Pydantic validates the structured AI assessment.
7. FastAPI returns the project details, risk classification, warnings, and AI recommendations.

## 4. Database Management

The application uses a separate Week 4 test database:

`october/week4/portfolio_test.db`

On the first run, the application copies the original September database:

`september/week2/portfolio.db`

If the Week 4 database already exists, the application reuses it rather than copying the source database again.

This separation allows testing of project creation, updates, and deletion without directly modifying the original September database.

## 5. API Endpoints

| HTTP Method | Endpoint | Purpose |
|---|---|---|
| GET | `/hello` | Returns a welcome message |
| GET | `/about` | Returns basic application information |
| GET | `/projects` | Retrieves all projects |
| GET | `/projects?status=Delayed` | Filters projects by status |
| GET | `/projects/{project_id}` | Retrieves a project by ID |
| POST | `/projects` | Creates a new project |
| PUT | `/projects/{project_id}` | Updates an existing project |
| DELETE | `/projects/{project_id}` | Deletes an existing project |
| GET | `/projects/{project_id}/analyze` | Calculates risk and generates an AI assessment |
| GET | `/ask-ai?question=...` | Answers a general project-management question using Gemini |

Interactive API documentation is available at `/docs` when the application is running locally.

## 6. Rule-Based Risk Assessment

The application calculates risk using explicit Python business rules.

| Condition | Risk |
|---|---|
| Project status is `On Track` | Low |
| Project status is `Delayed`, delay is greater than zero, and cost exceeds ₹10 lakh | High |
| Other cases | Medium |

The status check takes priority. Therefore, an `On Track` project receives Low risk even if its delay field contains a positive value.

The risk classification is calculated by Python and is separate from Gemini's assessment.

## 7. Data Consistency Checks

The application checks for an inconsistency when:

- Project status is `On Track`.
- Recorded delay is greater than zero.

When this condition occurs, the API returns a warning asking the user to verify the project status.

The application does not automatically change the project status or override the rule-based risk classification.

If the project is `On Track` with zero delay, the consistency-warning list is empty.

## 8. AI Assessment

The project-analysis endpoint sends the project data, rule-based risk, and consistency warnings to Gemini.

The AI assessment contains two structured fields:

- `key_concerns` — Potential concerns identified from the supplied information.
- `recommended_actions` — Practical actions suggested by the AI.

Pydantic validates the expected structure of the response.

The prompt instructs Gemini to use Indian Rupees (INR), avoid inventing missing project facts, and provide concise business recommendations.

AI-generated recommendations may vary between requests and should be reviewed before being used for business decisions.

## 9. Error Handling

The application handles the following situations:

- **HTTP 404:** Requested project does not exist.
- **HTTP 502:** Gemini API request fails or returns an invalid structured assessment.

Database errors and other unexpected failures may require additional error handling in a future iteration.

## 10. Testing and Results

The following scenarios were tested using the FastAPI Swagger interface.

| Test Scenario | Expected Result | Observed Result |
|---|---|---|
| Retrieve all projects | HTTP 200 and project list | Passed |
| Analyse Data Migration initially | Original project data, High risk, AI assessment | Passed |
| Update delay from 60 to 75 days | Successful update | Passed |
| Analyse after update | Latest delay of 75 days and High risk | Passed |
| Set status to `On Track` with 75 days of delay | Low risk and consistency warning | Passed |
| Set status to `On Track` with zero delay | Low risk and no consistency warnings | Passed |
| Analyse nonexistent project ID 999 | HTTP 404, `Project not found` | Passed |
| Verify AI currency formatting | Cost expressed in INR | Passed |

### End-to-End Workflow Demonstrated

The application successfully demonstrated the following workflow:

**Update project → Save to SQLite → Retrieve latest data → Calculate risk → Check consistency → Generate AI assessment**

## 11. Setup and Execution

### Prerequisites

- Python installed
- Project virtual environment configured
- Dependencies installed
- Valid Gemini API key

### Environment Configuration

Create a `.env` file in the repository root with:

`GEMINI_API_KEY=your_api_key_here`

Do not commit the `.env` file or expose the API key in source code.

### Run the Application

From the repository root, activate the virtual environment and run:

`python -m uvicorn october.week4.main:app --reload`

Open the following URL in a browser:

`http://127.0.0.1:8000/docs`

Use Swagger to execute and test the API endpoints.

## 12. Key Learnings

- Integrating REST APIs with persistent database operations.
- Applying deterministic business rules before invoking generative AI.
- Validating structured AI responses using Pydantic.
- Identifying data inconsistencies through explicit business logic.
- Handling common API and AI-service failures.
- Testing an end-to-end business workflow through Swagger.
- Separating test data from the original project database.

## 13. Future Improvements

Potential future enhancements include:

- Stronger validation of project status, cost, and delay values.
- More comprehensive database and API error handling.
- Explicit currency fields in the database.
- Improved AI evaluation and factual consistency checks.
- Automated tests for business rules and API endpoints.
- Logging and monitoring for production deployment.
- Authentication and authorization for project-management endpoints.

---

**Project:** AI-First Career — October Week 4  
**Focus:** End-to-end integration of APIs, databases, business rules, and generative AI.
