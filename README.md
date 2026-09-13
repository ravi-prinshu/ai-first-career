AI-First Career
A hands-on learning journey focused on becoming an **AI-first Business Analyst / Project Manager**.
The goal is to combine business analysis, consulting, project/program management, data, software development fundamentals,
and modern AI capabilities to build practical AI-enabled business solutions.
n Learning Objectives
The learning journey focuses on developing capabilities across:
• Business Analysis
• Project & Program Management
• Technology Consulting
• Python
• SQL & Data Analysis
• APIs & JSON
• LLMs & Generative AI
• Prompt Engineering
• RAG (Retrieval-Augmented Generation)
• AI Agents
• MCP (Model Context Protocol)
• AI-enabled business workflows
• Git & GitHub
• Application development fundamentals
n Learning Roadmap
August — Foundation
August focused on building the technical foundation required to start developing AI-enabled applications.
Week 1 — Development Environment & Git/GitHub
Git & GitHub
• Git and GitHub fundamentals
• Repository creation
• Git staging
• Commits
• Push to GitHub
Development Environment
• VS Code
• Python setup
• Development environment fundamentals
Week 2 — Python Basics
Development Environment
• Windows Terminal / PowerShell
• VS Code
• Python interpreter
• Virtual environments
• pip
• Installing Python packages
Python
• Running `.py` files
• `input()`
• `print()`
• Variables
• Strings
• Integers
• Basic calculations
• Type conversion with `int()`
• Conditional statements
• `if`, `elif`, `else`
• Comparison operators
• Boolean logic
• `and`, `or`, `not`
• Understanding syntax errors
• Understanding type errors
Git Workflow
• `git status`
• `git add`
• `git commit`
• `git push`
• `.gitignore`
• Virtual environment exclusion
AI-Assisted Development
• Writing requirements for AI
• Asking AI to generate code
• Reviewing AI-generated code
• Testing AI suggestions
• Debugging AI-generated/modified code
Mini Project — Profile Generator
Built a Python profile generator that:
• Accepts name, age and role
• Calculates age next year
• Displays a formatted profile
Week 3 — Python Core, JSON, Files & APIs
Topics Covered
• Python variables and data types
• Conditional statements
• Boolean logic
• Lists
• Dictionaries
• Lists of dictionaries
• `for` loops
• `while` loops
• Functions
• Parameters
• Arguments
• `return`
• JSON handling with Python
• `json.dumps()`
• `json.loads()`
• Reading files
• Writing files
• Appending to files
• File handling modes
• Using the `requests` library
• Making GET requests to APIs
• API response status codes
• Working with API responses
• Extracting data from JSON responses
• Combining APIs with Python logic
Mini Project — Project Risk Analyzer
Built a Python program that:
• Stores project risks in a list
• Classifies risks using conditions
• Uses a function to analyze risks
• Stores results in a dictionary
• Converts the dictionary to JSON
• Saves the risk report to a JSON file
• Reads the JSON file back into Python
• Extracts specific risk information
• Handles the complete flow from Python data → JSON → file → Python
Files
• `week3_basics.py` — Python basics practice
• `week3_lists.py` — Lists practice
• `week3_dictionary.py` — Dictionaries practice
• `week3_loops.py` — Loop practice
• `week3_functions.py` — Function practice
• `week3_json.py` — JSON practice
• `week3_files.py` — File handling practice
• `week3_api.py` — API and JSON response practice
• `week3_project.py` — Project Risk Analyzer
• `risk_report.json` — Generated project risk report
• `profile.txt` — File handling practice
Week 4 — AI Ecosystem Foundation
Week 4 focused on understanding the architecture and major building blocks behind modern AI applications.
REST APIs
• What an API is
• Client and server
• Request and response
• HTTP methods
- GET
- POST
- PUT
- PATCH
- DELETE
• HTTP status codes
- 200
- 201
- 400
- 401
- 403
- 404
- 500
• API → application → database architecture
Databases
• What databases are
• Relational databases
• Tables
• Rows
• Columns
• Primary keys
• SQL
• Introduction to NoSQL
• Understanding how APIs interact with databases
LLM Fundamentals
• What an LLM is
• Training vs inference
• Tokens
• Context window
• System messages
• User messages
• Hallucinations
• Business risks of incorrect AI-generated information
RAG — Retrieval-Augmented Generation
• What RAG is
• Why RAG is used
• Retrieval + context + generation
• Using company documents as a knowledge source
• Grounding LLM responses in external information
• RAG with PDFs, documents, databases and knowledge bases
• Introduction to:
- Document chunking
- Embeddings
- Vector databases
- Similarity search
- Context construction
AI Agents
• What an AI agent is
• Chatbots vs AI agents
• Tool usage
• Planning
• Multi-step workflows
• Memory/state
• Human-in-the-loop
• Agent decision-making
Example business workflow:
• Check project status
• Identify high-risk projects
• Prepare a summary
• Find the relevant stakeholder
• Send an update
MCP — Model Context Protocol
• What MCP is
• Why standardized tool connectivity matters
• MCP servers
• Tools and resources
• Connecting AI applications with external capabilities
Examples:
• Search documents
• Get project status
• Create an issue
• Send an email
Docker
• What Docker is
• Containers
• Images
• Application packaging
• Dependency consistency
• Difference between Python virtual environments and Docker
• Role of Docker in deploying AI applications
AI Application Architecture
High-level architecture understood during Week 4:
User
↓
Application / API
↓
AI Application
nnn Database
nnn RAG / Internal Knowledge
nnn AI Agent
nnn Tools / MCP
↓
LLM
↓
Response / Action
September — AI Application Development
September focuses on moving from Python fundamentals toward building practical AI applications.
Week 1 — Python Deepening
Topics
• Functions in greater depth
• Dictionaries as function arguments
• Returning multiple values
• Default parameters
• Reusable business logic
• Lists and dictionaries in real-world datasets
• Filtering structured data
• List comprehensions
• Error handling
• `try` / `except`
• `else`
• `finally`
• Raising exceptions
• Modules and imports
• Environment variables
• `.env` files
• API key security
• Debugging
• Tracebacks
• Syntax vs runtime vs logic errors
• Writing cleaner Python
• Meaningful variable names
• Functions with clear responsibilities
Mini Project — Project Data Processor
Build a Python application that processes structured project data and produces useful business insights.
Planned capabilities:
• Reading project data
• Processing multiple project records
• Filtering projects
• Calculating metrics
• Identifying delayed/high-risk projects
• Reusing logic through functions
• Handling errors
• Producing structured output
Week 2 — SQL & Data Analysis
Topics
• Database fundamentals
• SQL fundamentals
• `SELECT`
• `WHERE`
• `ORDER BY`
• `GROUP BY`
• `HAVING`
• Aggregate functions
• `COUNT`
• `SUM`
• `AVG`
• `MIN`
• `MAX`
• `JOIN`
• Subqueries
• Basic business analysis using SQL
Mini Project — Project Portfolio Analytics
Analyze a project portfolio to answer questions such as:
• How many projects are delayed?
• Which business units have the highest risk?
• What is the average project cost?
• Which projects have the highest cost?
• Which project managers have the most delayed projects?
• What percentage of projects are delayed?
Week 3 — LLM APIs & Prompt Engineering
Topics
• Calling an LLM API from Python
• API keys
• Environment variables
• System prompts
• User prompts
• Structured prompting
• Few-shot prompting
• Output formatting
• JSON/structured outputs
• Basic model parameters
• Temperature
• Token awareness
• Cost awareness
• Prompt evaluation
• Business-focused prompt design
Mini Project — AI Project Risk Analyzer
Build an AI-enabled version of the Project Risk Analyzer that uses an LLM to:
• Analyze project information
• Identify potential risks
• Summarize project risks
• Produce structured output
• Generate business-friendly recommendations
Week 4 — RAG Fundamentals & First RAG Application
Topics
• Document ingestion
• Document processing
• Chunking
• Embeddings
• Vector databases
• Similarity search
• Retrieval
• Context construction
• Grounded generation
• RAG architecture
• Hallucination mitigation
• Basic RAG evaluation
Mini Project — Internal Policy Assistant
Build a simple RAG application that can answer questions using internal policy documents.
Example questions:
• What is the leave policy?
• What is the travel reimbursement limit?
• What is the approval process?
• What documents are required?
• What happens if a request exceeds the defined limit?
n Future Roadmap
October — AI Agents & Workflows
Planned focus:
• AI agent architecture
• Tool calling
• Function calling
• Agent workflows
• Multi-step reasoning workflows
• External tools
• MCP
• Human-in-the-loop
• Agent memory/state
• AI workflow automation
• Building practical agentic applications
The progression will be:
Python
↓
APIs
↓
LLMs
↓
RAG
↓
AI Agents
↓
Agentic AI Applications
nn Technology Stack
The learning journey currently uses or plans to use:
• Python
• SQL
• Git
• GitHub
• VS Code
• REST APIs
• JSON
• LLM APIs
• RAG
• Vector databases
• AI Agents
• MCP
• Docker
n Repository Structure
AI-First-Career/
n
nnn .venv/
nnn .vscode/
nnn .gitignore
nnn README.md
n
nnn august/
n nnn week1/
n n nnn hello.py
n n
n nnn week2/
n n nnn practice.py
n n nnn profile.py
n n
n nnn week3/
n n nnn profile.txt
n n nnn risk_report.json
n n nnn week3_api.py
n n nnn week3_basics.py
n n nnn week3_dictionary.py
n n nnn week3_files.py
n n nnn week3_functions.py
n n nnn week3_json.py
n n nnn week3_lists.py
n n nnn week3_loops.py
n n nnn week3_project.py
n n
n nnn week4/
n
nnn september/
nnn week1/
n Learning Philosophy
The learning journey is focused on **practical application rather than theory alone**.
Each stage follows:
Learn the concept
↓
Understand why it matters
↓
Practice with small examples
↓
Apply it to a business scenario
↓
Build a mini project
↓
Document the learning
↓
Commit to GitHub
The goal is not simply to learn Python or AI tools, but to develop the ability to **identify business problems, design AI-enabled
solutions, build working prototypes, and communicate the business value of those solutions.**
n Current Progress
August
n Development environment
n Git & GitHub fundamentals
n Python basics
n Virtual environments
n Lists & dictionaries
n Loops
n Functions
n JSON
n File handling
n REST APIs
n API responses & status codes
n Database fundamentals
n LLM fundamentals
n RAG fundamentals
n AI Agent fundamentals
n MCP fundamentals
n Docker fundamentals
n Project Risk Analyzer
September
n Functions — deeper concepts
n Lists & dictionaries — deeper concepts
n List comprehensions
n Error handling
n Modules & imports
n Environment variables
n Debugging & clean Python
n Project Data Processor
n SQL & Data Analysis
n LLM APIs & Prompt Engineering
n RAG Application
n End Goal
Build the skills required to become an **AI-first BA / PM / Technology Consultant** who can:
• Understand modern AI architectures
• Work effectively with developers and AI engineers
• Analyze business and project data
• Use Python and SQL for practical analysis
• Work with LLM APIs
• Design effective prompts
• Build RAG applications
• Understand and build AI agent workflows
• Connect AI systems with external tools
• Prototype AI-enabled business solutions
• Evaluate AI outputs and business risks
• Translate business problems into practical AI solutions