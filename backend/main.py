from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import get_answer

app = FastAPI()

# ✅ CORS – MUST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Vercel URL potaalum ok
    allow_credentials=True,
    allow_methods=["*"],          # 👈 OPTIONS allow aagum
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    answer = get_answer(query.question)
    return {"answer": answer}

# 👇 OPTIONAL: root route (404 avoid panna)
@app.get("/")
def root():
    return {"status": "RAG API running"}
