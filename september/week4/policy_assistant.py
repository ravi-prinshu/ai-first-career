import chromadb
from google import genai


def search_policy(question, top_k=3, threshold=0.60):
    """Search the policy database and return relevant chunks."""

    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(
        name="internal_policy"
    )

    gemini_client = genai.Client()

    # Convert the question into an embedding
    embedding_result = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    question_embedding = embedding_result.embeddings[0].values

    # Search Chroma
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    # Build clean result objects
    search_results = []

    for i in range(len(results["ids"][0])):
        search_results.append({
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i],
            "title": results["metadatas"][0][i]["title"],
            "page": results["metadatas"][0][i]["page"]
        })

    # Keep only results below the distance threshold
    filtered_results = [
        result
        for result in search_results
        if result["distance"] <= threshold
    ]

    return filtered_results


def build_context(results):
    """Combine retrieved policy chunks into LLM context."""

    return "\n\n".join(
        result["text"]
        for result in results
    )


def generate_answer(question, context):
    """Generate a grounded answer using the retrieved context."""

    gemini_client = genai.Client()

    prompt = f"""
Answer the question using only the retrieved policy context.

Do not use any information outside the provided context.

If the answer cannot be found in the provided context, say:
"I don't have enough information in the provided context."

Give a concise and useful answer.

Context:
{context}

Question:
{question}
"""

    response = gemini_client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


def main():

    print("Policy Assistant ready")

    question = input("\nAsk a policy question: ")

    filtered_results = search_policy(question)

    print("\nRetrieved Sources:")

    for result in filtered_results:
        print(
            f"- {result['title']} — "
            f"Page {result['page']} "
            f"(distance: {result['distance']:.4f})"
        )

    context = build_context(filtered_results)

    answer = generate_answer(question, context)

    print("\nAnswer:")
    print(answer)

    print("\nSources:")

    for result in filtered_results:
        print(
            f"- {result['title']} — Page {result['page']}"
        )


if __name__ == "__main__":
    main()