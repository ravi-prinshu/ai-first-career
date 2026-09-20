from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Explain what a Business Analyst does in one sentence."
)

print(response.output_text)