from google import genai

client = genai.Client()

text = "Employees receive 20 days of annual leave."

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text
)

embedding = result.embeddings[0].values

print("Number of dimensions:", len(embedding))
print("First 10 values:", embedding[:10])