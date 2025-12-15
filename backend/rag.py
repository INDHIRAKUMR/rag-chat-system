import os
import pickle
import faiss
import numpy as np
import torch

from transformers import AutoTokenizer, AutoModel
from groq import Groq

# ---------------------------
# CONFIG
# ---------------------------
VECTOR_DIR = "vectorstore"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------------------
# LOAD EMBEDDING MODEL
# ---------------------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

# ---------------------------
# GROQ CLIENT
# ---------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------
# LOAD FAISS + DATA
# ---------------------------
index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))

with open(os.path.join(VECTOR_DIR, "store.pkl"), "rb") as f:
    texts, sources = pickle.load(f)

# ---------------------------
# EMBEDDING FUNCTION
# ---------------------------
def embed_text(text: str) -> np.ndarray:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # Mean pooling
    embeddings = outputs.last_hidden_state.mean(dim=1)

    return embeddings.cpu().numpy()

# ---------------------------
# MAIN RAG FUNCTION
# ---------------------------
def get_answer(query: str) -> str:
    query_embedding = embed_text(query)

    _, indices = index.search(query_embedding, 4)

    context = "\n".join([texts[i] for i in indices[0]])

    prompt = f"""
You are a professional business support assistant.
Answer ONLY using the context below.
If the answer is not found, say you will connect to human support.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
