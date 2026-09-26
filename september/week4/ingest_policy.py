import chromadb
from google import genai

from policy_data import policy_sections


# -----------------------------
# 1. Connect to Chroma
# -----------------------------

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="internal_policy"
)


# -----------------------------
# 2. Connect to Gemini
# -----------------------------

gemini_client = genai.Client()


# -----------------------------
# 3. Prepare policy chunks
# -----------------------------

texts = [
    section["text"].strip()
    for section in policy_sections
]


# -----------------------------
# 4. Generate embeddings
#    for all chunks at once
# -----------------------------

embedding_result = gemini_client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts
)

embeddings = [
    embedding.values
    for embedding in embedding_result.embeddings
]


# -----------------------------
# 5. Store chunks in Chroma
# -----------------------------

ids = [
    f"policy_{i + 1}"
    for i in range(len(policy_sections))
]

metadatas = [
    {
        "title": section["title"],
        "page": section["page"]
    }
    for section in policy_sections
]

collection.add(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas
)


print(f"Successfully added {len(texts)} policy chunks to Chroma.")