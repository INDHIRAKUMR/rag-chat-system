from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag import get_answer

app = FastAPI()

# CORS settings
origins = [
    "*",  # illa specific frontend URL kudunga for security
    # "http://localhost:5174",  # dev time
    # "https://your-frontend-vercel-url.com"  # production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    answer = get_answer(query.question)
    return {"answer": answer}
