from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag import get_answer

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    answer = get_answer(query.question)
    return {"answer": answer}
