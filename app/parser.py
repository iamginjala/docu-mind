from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymupdf4llm
import os

def process_document(path):
    """
    convert the given .pdf or .txt files into text file using pymupdf4llm or 
    Recursive character text splitter
    """
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=50,
    length_function=len,
    )
    if path.endswith(".pdf"):
        txt = pymupdf4llm.to_text(path)
        filename = os.path.basename(path)
        texts = text_splitter.create_documents([txt])
        return filename,texts
    
    elif path.endswith(".txt"):
        filename = os.path.basename(path)
        with open(path,encoding="utf-8") as f:
            txt = f.read()
        texts = text_splitter.create_documents([txt])
        return filename,texts
    
    else:
        raise ValueError("only pdf and text files")