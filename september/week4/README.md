# September Week 4 — RAG Fundamentals + Internal Policy Assistant

## Objective

Build a simple Retrieval-Augmented Generation (RAG) application that can answer questions using an internal policy knowledge base.

The project demonstrates:

- Document ingestion
- Chunking
- Embeddings
- Vector similarity search
- Persistent vector storage
- Retrieval
- Context augmentation
- Grounded LLM generation
- Source attribution
- Basic RAG evaluation

---

## RAG Architecture

```text
Policy Data
    ↓
Semantic Chunks
    ↓
Gemini Embeddings
    ↓
Chroma Vector Database
    ↓
User Question
    ↓
Question Embedding
    ↓
Similarity Search
    ↓
Distance Threshold
    ↓
Relevant Context
    ↓
Gemini LLM
    ↓
Grounded Answer
    ↓
Source Attribution

Project Structure

week4/
│
├── policy_data.py
├── ingest_policy.py
├── policy_assistant.py
├── embedding_test.py
├── chroma_test.py
└── chroma_db/

Key files

policy_data.py

Contains the synthetic internal company policy used for the project.

ingest_policy.py

Creates embeddings for the policy chunks and stores them in Chroma.

policy_assistant.py

Retrieves relevant policy information and generates a grounded answer using Gemini.

embedding_test.py

Used to understand text embeddings and inspect embedding dimensions.

chroma_test.py

Used to experiment with persistent Chroma storage and similarity search.

Policy Knowledge Base

The synthetic policy contains five sections:

Annual Leave
Sick Leave
Business Travel
Hotel Expenses
Work From Home

Each section contains:

Policy text
Title
Page number
Embeddings

The project uses:

gemini-embedding-001

Embeddings convert text into numerical vectors that represent semantic meaning.

The same embedding model is used for:

Policy chunks during ingestion
User questions during retrieval

Document embeddings are generated during ingestion and stored in Chroma.

A new embedding is generated for each user question.

Vector Database

The project uses:

Chroma

with a persistent local database.

chromadb.PersistentClient(path="./chroma_db")

This means the stored embeddings remain available after the Python program exits.

This avoids regenerating document embeddings every time the assistant starts.

Retrieval

The application retrieves the top matching policy chunks from Chroma.

Chroma returns a distance value.

For this project:

Lower distance = greater similarity

A temporary experimental threshold of:

0.60

is used to filter retrieved results.

This threshold was selected for experimentation with the synthetic dataset and should not be treated as a universal production threshold.

Grounded Generation

The retrieved policy chunks are passed to Gemini as context.

The prompt instructs the model to:

Use only the retrieved policy context
Avoid using information outside the context
State when the information is unavailable
Provide a concise answer

This reduces the risk of the model inventing policy information.

Source Attribution

The application keeps source metadata separately from the LLM context.

Each retrieved result contains:

Title
Page
Distance
Policy text

The final application output displays the relevant source and page number.

Example:

Answer:
The hotel expense reimbursement limit is up to ₹8,000 per night.

Sources:
- Hotel Expenses — Page 2

This provides basic traceability for the generated answer.

RAG Evaluation

Five questions were used to test the system.

Test	Expected behavior	Result
How many annual leave days do employees receive?	20 days	✅
Can unused annual leave be carried forward?	Up to 5 days	✅
When can employees use business class?	6 hours or longer	✅
What is the hotel expense reimbursement limit?	₹8,000/night	✅
What is the company's parental leave policy?	Insufficient information	✅
Important observation

The parental leave question was intentionally not included in the policy data.

The system retrieved no chunks below the configured distance threshold and generated:

I don't have enough information in the provided context.

This demonstrates basic grounded behavior for an unanswerable question.

Key Learnings
1. RAG vs normal prompting

Instead of relying entirely on information already known by the LLM, RAG retrieves relevant external information and provides it as context.

2. RAG vs fine-tuning

RAG is useful when the application needs access to changing or external knowledge.

Fine-tuning is more focused on changing model behavior, style, or task patterns.

3. Chunking

Documents should be divided into meaningful semantic chunks.

For this small policy dataset, each policy section was already a coherent chunk, so further splitting was unnecessary.

4. Embeddings

Embeddings represent semantic meaning numerically and allow questions to be matched with relevant text.

5. Vector similarity

Semantic similarity allows a question such as:

How many vacation days do employees get?

to match policy text containing:

Employees receive 20 days of annual leave.

even though the wording is different.

6. Persistent vector storage

Document embeddings should generally be created during ingestion/update rather than regenerated for every user question.

7. Grounding

Retrieval alone does not guarantee a correct answer.

The application also needs:

Relevant retrieval
Appropriate context
Grounded prompting
Evaluation
8. Metadata

Metadata such as source and page number enables basic traceability and supports auditing and debugging.

API Efficiency

Gemini embedding calls were batched during ingestion rather than making one API request per policy chunk.

The vector database is persistent, so document embeddings do not need to be regenerated for every query.

Only the user's question requires a new embedding during normal retrieval.

This reduces unnecessary API usage.

Technologies Used
Python
Gemini API
Gemini Embeddings
ChromaDB
Pydantic concepts from Week 3
Vector similarity search
Retrieval-Augmented Generation (RAG)
Project Outcome

Built a working local RAG-based Internal Policy Assistant capable of:

Storing policy knowledge as vector embeddings
Searching the policy database semantically
Filtering results using a distance threshold
Providing retrieved context to an LLM
Generating grounded answers
Providing source/page attribution
Handling questions outside the available knowledge base

