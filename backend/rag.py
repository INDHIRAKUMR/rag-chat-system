import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq

BASE_DIR = os.path.dirname(__file__)
VECTOR_DIR = os.path.join(BASE_DIR, "vectorstore")

model = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))

with open(os.path.join(VECTOR_DIR, "store.pkl"), "rb") as f:
    texts, sources = pickle.load(f)

def get_answer(query: str) -> str:
    query_embedding = model.encode([query])
    _, indices = index.search(query_embedding, 4)

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
