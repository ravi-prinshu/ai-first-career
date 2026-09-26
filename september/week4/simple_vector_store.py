from google import genai
import math

client = genai.Client()


documents = [
    "Employees receive 20 days of annual leave.",
    "International business travel requires prior approval.",
    "Employees can claim hotel expenses up to ₹8,000 per night."
]


def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (magnitude_a * magnitude_b)


# Create our simple vector store
vector_store = []

for document in documents:

    embedding = get_embedding(document)

    vector_store.append({
        "text": document,
        "embedding": embedding
    })

def search(query, top_k=2):

    query_embedding = get_embedding(query)

    results = []

    for item in vector_store:

        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        results.append({
            "text": item["text"],
            "similarity": similarity
        })

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results[:top_k]

print("Documents stored:", len(vector_store))

question = "How many vacation days do employees get?"

results = search(question, top_k=2)

print("\nSearch Results:")

for result in results:

    print(
        f"{result['similarity']:.4f} | "
        f"{result['text']}"
    )