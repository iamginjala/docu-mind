from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from embeddings import search_similar
from google import genai
import os
from dotenv import load_dotenv



load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

class DocuMindState(TypedDict):
    question : str
    chunks: list
    answer: str
    chat_history: list
def retrieve_chunks(state: DocuMindState) -> dict:
    chunk = search_similar(state["question"])
    return {"chunks":chunk}
def generate_answer(state: DocuMindState):
    prompt = f""" You are a helpful assistant that answers questions based on the provided document context.

    CONTEXT:
    {state['chunks']}

    CHAT HISTORY:
    {state['chat_history']}

    CURRENT QUESTION:
    {state['question']}

   Instructions: 
   - Only answer based on the context provided
   - If the context does not contain relevant information, say "the information is not in the file" 
   - Keep your answer clear and simple
   """
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents = prompt
    )
    return {"answer":response.text}
def update_memory(state: DocuMindState):
    question = state["question"]
    answer = state["answer"]
    state["chat_history"].append((question,answer))
    history = state["chat_history"]

    return {"chat_history":history[-5:]}

graph = StateGraph(DocuMindState)

graph.add_node("retrieve_chunks", retrieve_chunks)
graph.add_node("generate_answer", generate_answer)
graph.add_node("update_memory", update_memory)

graph.add_edge("retrieve_chunks","generate_answer")
graph.add_edge("generate_answer","update_memory")

graph.add_edge(START, "retrieve_chunks")
graph.add_edge("update_memory", END)


app = graph.compile()


result = app.invoke({
    "question": "what is the methodology used in their work?",
    "chunks": [],
    "answer": "",
    "chat_history": []
})
