from google import genai
import math

client = genai.Client()

documents = [
    {
        "text": "Employees receive 20 days of annual leave.",
        "source": "Employee Leave Policy.pdf",
        "page": 12
    },
    {
        "text": "International business travel requires prior approval.",
        "source": "Travel Policy.pdf",
        "page": 8
    },
    {
        "text": "Employees can claim hotel expenses up to ₹8,000 per night.",
        "source": "Travel Policy.pdf",
        "page": 10
    }
]

def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b)

vector_store = []

for document in documents:
    embedding = get_embedding(document["text"])

    vector_store.append({
        "text": document["text"],
        "embedding": embedding,
        "source": document["source"],
        "page": document["page"]
    })

def search(query, top_k=3, threshold=0.70):

    query_embedding = get_embedding(query)
    results = []

    for item in vector_store:

        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        results.append({
            "text": item["text"],
            "similarity": similarity,
            "source": item["source"],
            "page": item["page"]
        })

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )


    top_results = results[:top_k]

    filtered_results = [
        result for result in top_results
        if result["similarity"] >= threshold
    ]

    return filtered_results

question = "How many vacation days do employees get?"

results = search(question, top_k=2)

if not results:
    print("I don't have enough information in the provided documents.")

else:
    context = "\n".join(
        result["text"] for result in results
    )

    print("Retrieved Context:")
    print(context)

    prompt = f"""
    Answer the question using only the retrieved context.

    Do not use any information outside the provided context.

    If the answer cannot be found in the retrieved context, say:
    "I don't have enough information in the provided context."

    Give a concise and useful answer.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    print("\nFull Results:")
    for result in results:
        print(result)
    print("\nAnswer:")
    print(response.text)