from fastapi import FastAPI,UploadFile
from pydantic import BaseModel
from typing import Annotated,List
from app.embeddings import generate_embeddings, store_embeddings
from app.parser import process_document
from app.rag import app as rag_app
import os
from contextlib import asynccontextmanager
from app.db import init_db


class Question(BaseModel):
    ques: str
    chat_history: list = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # runs when FastAPI starts
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_documents(files: List[UploadFile]):
    upload_directory = "documents"
    os.makedirs(upload_directory,exist_ok=True)
    for file in files:
        file_location = f"{upload_directory}/{file.filename}"
        with open (file_location, "wb") as buffer:
            buffer.write(await file.read())
        filename,chunks = process_document(file_location)
        content,embeddings = generate_embeddings(chunks)
        store_embeddings(content,embeddings,filename)
    
    return {"message": "successfully processed", "files": [file.filename for file in files]}

@app.post("/ask")
async def llm_response(question: Question):
    result = rag_app.invoke({
      "question": question.ques,
      "chunks": [],
      "answer": "",
      "chat_history": question.chat_history
    })
    return {"answer": result["answer"],"chat_history": result["chat_history"]}

