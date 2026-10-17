# October Week 3 — AI-Powered Project Risk Analysis

## Objective

Build a FastAPI application that retrieves project data from SQLite, uses Gemini to generate a structured risk analysis, and combines AI recommendations with deterministic business rules.

## Architecture

Client → FastAPI → SQLite → Python Business Rules → Gemini API → Structured JSON Response

## What I Learned

### 1. Gemini API Integration
- Loaded the Gemini API key from a root `.env` file using `python-dotenv`.
- Used an environment variable to avoid hardcoding the API key.
- Made successful Gemini API requests from Python.

### 2. FastAPI Integration
- Created endpoints that accept user requests and return JSON.
- Built `/ask-ai` to answer general business questions.
- Built `/projects/{project_id}/analyze` for project-specific analysis.

### 3. Database-Grounded AI
- Retrieved project records from the existing SQLite portfolio database.
- Passed actual project details to Gemini rather than asking it to guess.
- Returned HTTP 404 when a requested project did not exist.

### 4. Prompt Engineering
- Used role, context, task, and output instructions to guide Gemini.
- Improved responses by requesting concise, business-oriented recommendations.

### 5. Structured Output and Pydantic
- Defined an `AIProjectAssessment` model.
- Requested JSON output from Gemini.
- Validated the response using Pydantic.
- Returned concerns and recommendations as separate lists.

### 6. Deterministic Business Rules
Implemented the existing portfolio risk rules:

- No delay → Low Risk
- Delayed and cost greater than ₹10 lakh → High Risk
- Delayed and cost at or below ₹10 lakh → Medium Risk

The rule-based classification remains separate from Gemini's analysis.

### 7. Error Handling
- Preserved the 404 response for missing projects.
- Added handling for Gemini API errors using HTTP 502.

## Tests Performed

| Test | Expected result |
|---|---|
| `GET /ask-ai` with a business question | HTTP 200 with an AI-generated answer |
| `GET /projects/3/analyze` | HTTP 200 with project data, rule-based risk, and structured AI assessment |
| `GET /projects/99/analyze` | HTTP 404 — Project not found |

## Key Business and Technical Lessons

- AI should be grounded in verified application data.
- Deterministic rules should remain authoritative for predefined business decisions.
- Pydantic validates response structure, not factual correctness.
- Prompt instructions guide AI output but do not guarantee perfect compliance.
- API error handling improves the clarity of failures for clients.

## Security

- API credentials are loaded from `.env`.
- The root `.gitignore` excludes `.env`.
- Never commit API keys or other secrets.

## Outcome

Built a working AI-enabled business application that combines Python, FastAPI, SQLite, Gemini, Pydantic, and predefined business rules to produce structured project risk analysis.
