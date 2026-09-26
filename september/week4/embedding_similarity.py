from google import genai
import math

client = genai.Client()


documents = [
    "Employees receive 20 days of annual leave.",
    "International business travel requires prior approval.",
    "Employees can claim hotel expenses up to ₹8,000 per night."
]

question = "How many vacation days do employees get?"


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


question_embedding = get_embedding(question)

for i, document in enumerate(documents):

    document_embedding = get_embedding(document)

    similarity = cosine_similarity(
        question_embedding,
        document_embedding
    )

    print(
        f"Chunk {i + 1}: "
        f"{similarity:.4f} | "
        f"{document}"
    )