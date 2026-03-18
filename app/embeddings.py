from parser import process_document
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from db import connect_db

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))


def generate_embeddings(chunks):
    content = [i.page_content for i in chunks]
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=content,
        config=types.EmbedContentConfig(output_dimensionality=1536)
    )

    return content,result.embeddings

def store_embeddings(content,embeddings,filename):
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(len(embeddings)):
        cursor.execute( "INSERT INTO documents (metadata,contents,embeddings) VALUES (%s, %s, %s)",
                   (filename,content[i],list(embeddings[i].values)))
    conn.commit()
    cursor.execute("select * from documents;")
    rows = cursor.fetchall()

    for i in rows:
        print(i)
    cursor.close()
    conn.close()

    return True

chunks = process_document('documents/grass.txt')
content,embeddings = generate_embeddings(chunks)
print(store_embeddings(content,embeddings,"grass.txt"))