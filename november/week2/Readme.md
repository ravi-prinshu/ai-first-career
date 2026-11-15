
# November – Week 2: Python Tools and Gemini Tool Selection

## Objective

Build reusable Python functions, expose them to Gemini through function declarations, and test Gemini's ability to select appropriate tools based on user requests.

## 1. Python Tools

Created three reusable functions in `tools.py`.

| Function | Purpose |
|---|---|
| get_project_details(project_id) | Retrieves details of an individual project |
| list_projects(status=None) | Retrieves all projects or filters by status |
| calculate_project_risk(project_id) | Calculates project risk using cost and delay |

### Project Risk Rules

- High: Delayed project with cost greater than ₹10 lakh.
- Medium: Delayed project with cost of ₹10 lakh or less.
- Low: Project with zero delay days.

All three functions were tested with valid and invalid inputs.

## 2. Gemini Tool Schemas

Created `tool_schemas.py` using the Google Gen AI SDK.

Each tool declaration contains:
- Function name
- Function description
- Parameter names
- Parameter data types
- Required and optional parameters

The three declarations are registered together using `types.Tool`.

## 3. Python Tool Executor

Created `tool_executor.py`.

Key concepts:
- Function mapping using a Python dictionary.
- Allowlist of approved Python functions.
- Dynamic function selection.
- Dictionary unpacking using **kwargs.
- Error handling for unknown tools and invalid arguments.

The executor was independently tested using manually supplied function names and arguments.

## 4. Gemini Tool Selection

Created `gemini_tool_selection.py`.

Connected Gemini to the three tool declarations using the Google Gen AI SDK.

Automatic function execution was disabled so that Gemini's tool-call requests could be inspected independently.

### Test Results

| User Request | Selected Tool | Result |
|---|---|---|
| Show all delayed projects | list_projects | Passed |
| Calculate risk of project 4 | calculate_project_risk | Passed |
| Show all projects | list_projects | Passed |
| Review project 3 before management meeting | get_project_details and calculate_project_risk | Passed |
| Give complete details of project 3 | get_project_details | Passed |

### Important Observations

1. Gemini can select tools based on descriptions and user intent.
2. Optional parameters can be omitted.
3. Gemini can request multiple tools in a single response.
4. Tool selection and tool execution are separate operations.
5. Python remains responsible for executing approved functions.

## 5. Project Structure

november/
└── week2/
    ├── tools.py
    ├── tool_schemas.py
    ├── tool_executor.py
    ├── gemini_tool_selection.py
    └── README.md

## 6. Key Learnings

- Python function reuse and modularity.
- Function declarations and tool schemas.
- Function mapping and dynamic execution.
- Keyword argument unpacking.
- LLM tool selection.
- Independent versus sequential tool calls.
- Separation of AI reasoning and deterministic business logic.

## 7. Pending Work

The following activities are planned for November Week 3:

- Parse actual Gemini function-call responses.
- Execute Gemini-requested Python functions.
- Send execution results back to Gemini.
- Complete the tool-calling loop.
- Handle multiple and sequential tool calls.
- Test errors and document the integrated application.

## Completion Status

November Week 2 foundation and Gemini tool-selection tests completed.
