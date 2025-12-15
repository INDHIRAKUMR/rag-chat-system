import os
import pickle
import faiss
import numpy as np
from fastembed import TextEmbedding
from groq import Groq

VECTOR_DIR = "backend/vectorstore"

embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))

with open(os.path.join(VECTOR_DIR, "store.pkl"), "rb") as f:
    texts, sources = pickle.load(f)

def get_answer(query: str) -> str:
    query_vector = list(embedder.embed([query]))[0]
    query_vector = np.array([query_vector]).astype("float32")

    _, indices = index.search(query_vector, 4)

    context = "\n".join(texts[i] for i in indices[0])

    prompt = f"""
You are a professional business support assistant.
Answer only using the context below.
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
