import os
import pickle
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

DATA_DIR = "data"
VECTOR_DIR = "vectorstore"

os.makedirs(VECTOR_DIR, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []
sources = []

for file in os.listdir(DATA_DIR):
    if file.endswith(".pdf"):
        reader = PdfReader(os.path.join(DATA_DIR, file))
        for page in reader.pages:
            text = page.extract_text()
            if text and len(text.strip()) > 50:
                texts.append(text)
                sources.append(file)

print(f"Total chunks: {len(texts)}")

embeddings = model.encode(texts, show_progress_bar=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, os.path.join(VECTOR_DIR, "index.faiss"))

with open(os.path.join(VECTOR_DIR, "store.pkl"), "wb") as f:
    pickle.dump((texts, sources), f)

print("✅ PDF ingestion completed successfully")
