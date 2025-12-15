from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import get_answer

app = FastAPI(
    title="RAG Chat API",
    version="1.0.0"
)

# ✅ CORS (Vercel + Localhost safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production la specific URL kudukalaam
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request schema (FRONTEND MATCH)
class Query(BaseModel):
    query: str

@app.get("/")
def root():
    return {"status": "RAG backend running"}

@app.post("/ask")
def ask(data: Query):
    try:
        answer = get_answer(data.query)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
