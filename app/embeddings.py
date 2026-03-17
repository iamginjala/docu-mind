from parser import process_document
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))


def generate_embeddings(chunks):
    content = [i.page_content for i in chunks]
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=content,
    )
    return result.embeddings

chunks = process_document('./grass.txt')
embeddings = generate_embeddings(chunks)
print(f"Number of embeddings: {len(embeddings)}")
print(f"First embedding type: {type(embeddings[0])}")
print(f"First embedding values (first 5 numbers): {embeddings[0].values[50:60]}")


