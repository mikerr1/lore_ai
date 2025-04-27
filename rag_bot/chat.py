import os

import gradio as gr
import requests
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from settings import LORE_DB_DIR

# Set the LLM model for chat
LLM_MODEL = os.environ.get("LLM_MODEL")

# Setup
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    collection_name="lore_collection",
    embedding_function=embedding_model,
    persist_directory=LORE_DB_DIR
)

def chat(user_input, history=None):
    # Step 1: Embed and search lore
    docs = db.similarity_search(user_input, k=4)
    context = "\n\n".join(doc.page_content for doc in docs)

    # Step 2: Build prompt
    prompt = f"""You are an expert in the following universe/lore. 
    Answer truthfully based on the context information provided.
    Cited the reference such as chapter number, or page number.

        CONTEXT:
        {context}

        QUESTION:
        {user_input}

        Answer:"""

    # Step 3: Send to local LLM (example for Ollama)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma3:4b", "prompt": prompt, "stream": False}
    )

    if response.ok:
        return response.json()["response"]
    else:
        return "❌ Error communicating with the local LLM."

# Launch Gradio UI
gr.ChatInterface(chat).launch()
