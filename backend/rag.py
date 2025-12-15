import os
import pickle
import faiss
from fastembed import TextEmbedding
from groq import Groq

BASE_DIR = os.path.dirname(__file__)
VECTOR_DIR = os.path.join(BASE_DIR, "vectorstore")

embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))

with open(os.path.join(VECTOR_DIR, "store.pkl"), "rb") as f:
    texts, sources = pickle.load(f)

def get_answer(query: str) -> str:
    query_embedding = list(embedder.embed([query]))[0]
    _, indices = index.search(
        faiss.vector_to_array(query_embedding).reshape(1, -1), 4
    )

    context = "\n".join([texts[i] for i in indices[0]])

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
        temperature=0.2,
    )

    return response.choices[0].message.content
