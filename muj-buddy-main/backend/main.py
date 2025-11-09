from fastapi import FastAPI, Query
import pandas as pd
from pydantic import BaseModel
import os

app = FastAPI(title="MUJ Buddy (demo)")

# Load CSV at startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROF_CSV = os.path.join(BASE_DIR, "..", "data", "professors.csv")
PROF_CSV = os.path.normpath(PROF_CSV)

df = pd.read_csv(PROF_CSV)

@app.get("/api/find_professor")
def find_professor(name: str = Query(..., description="Professor name to search")):
    # simple case-insensitive search
    matches = df[df['name'].str.contains(name, case=False, na=False)]
    if matches.empty:
        return {"error": "Professor not found"}
    result = matches.to_dict(orient="records")
    return {"results": result}

class ChatRequest(BaseModel):
    query: str

@app.post("/api/chat")
def chat(req: ChatRequest):
    # Placeholder simple chat implementation — returns FAQ match or echo
    q = req.query.lower()
    # naive FAQ search
    with open("data/faq.txt", "r", encoding="utf-8") as f:
        faqs = f.read().lower()
    if q in faqs:
        return {"answer": "Found in FAQ: " + q}
    return {"answer": "Sorry, this is a demo chat. Replace with your RAG pipeline."}
