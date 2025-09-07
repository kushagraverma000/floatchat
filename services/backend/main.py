# services/backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document


app = FastAPI(title="FloatChat API")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to FloatChat API"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

class QueryRequest(BaseModel):
    query: str

# Load vector store
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="db",
    embedding_function=embedding_model,
    collection_name="argo_profiles"
)

docs = [
    Document(
        page_content="Warm salty water in the Indian Ocean",
        metadata={
            "date_time": "2023-05-01T12:00:00",
            "latitude": -20.1,
            "longitude": 65.3,
            "temperature_mean": 28.4,
            "salinity_mean": 35.2,
        }
    ),
    Document(
        page_content="Cold fresh water in the Pacific Ocean",
        metadata={
            "date_time": "2023-06-15T06:00:00",
            "latitude": 10.5,
            "longitude": -150.2,
            "temperature_mean": 15.1,
            "salinity_mean": 33.8,
        }
    ),
]

vectorstore.add_documents(docs)

@app.post("/search")
def search(req: QueryRequest):
    results = vectorstore.similarity_search_with_score(req.query, k=5)
    print("Chroma Collections:", vectorstore._collection.count())

    data = []
    for doc, score in results:
        print("DEBUG DOC:", doc.metadata)  
        meta = doc.metadata
        meta["score"] = round(score, 3)
        data.append(meta)
    return data