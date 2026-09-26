import chromadb
from google import genai

# -----------------------------
# 1. Connect to persistent Chroma DB
# -----------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="policy_documents"
)

print("Connected to Chroma")


# -----------------------------
# 2. Connect to Gemini
# -----------------------------

gemini_client = genai.Client()


# -----------------------------
# 3. User question
# -----------------------------

question = "How many vacation days do employees get?"


# -----------------------------
# 4. Create embedding for question
# -----------------------------

question_result = gemini_client.models.embed_content(
    model="gemini-embedding-001",
    contents=question
)

question_embedding = question_result.embeddings[0].values


# -----------------------------
# 5. Search Chroma
# -----------------------------

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=2
)


# -----------------------------
# 6. Display raw results
# -----------------------------

print("\nSearch Results:")
print(results)


# -----------------------------
# 7. Convert results into
#    cleaner structure
# -----------------------------

print("\nClean Search Results:")

clean_results = []

for i in range(len(results["ids"][0])):

    result = {
        "id": results["ids"][0][i],
        "text": results["documents"][0][i],
        "distance": results["distances"][0][i],
        "source": results["metadatas"][0][i]["source"],
        "page": results["metadatas"][0][i]["page"]
    }

    clean_results.append(result)

    print(result)


# -----------------------------
# 8. Apply distance threshold
# -----------------------------

threshold = 0.6

filtered_results = []

for result in clean_results:

    if result["distance"] <= threshold:
        filtered_results.append(result)


# -----------------------------
# 9. Display filtered results
# -----------------------------

print("\nFiltered Results:")

for result in filtered_results:
    print(result)