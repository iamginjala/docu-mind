from app.parser import process_document
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from app.db import connect_db

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
    cursor.close()
    conn.close()

    return True

def generate_question_embeddings(question):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question,
        config=types.EmbedContentConfig(output_dimensionality=1536)
    )
    return result.embeddings

def search_similar(question):
    question_embeddings = generate_question_embeddings(question)
    ques_embeddings = list(question_embeddings[0].values)
    conn = connect_db()
    cursor = conn.cursor()
    query = "select contents from documents where (1-(embeddings <=> (%s::vector))) > 0.3 order by embeddings <=> (%s::vector) asc limit 5;"
    cursor.execute(query,(ques_embeddings,ques_embeddings))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()


    return [row[0] for row in rows]
