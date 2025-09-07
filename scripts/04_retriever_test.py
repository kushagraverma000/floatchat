# scripts/04_retriever_test.py

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from chromadb.config import Settings
import chromadb
import os

def main():
    # Set path to your local Chroma DB
    db_path = os.path.join(os.getcwd(), "db")

    # Load embedding model (same one used before)
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Load Chroma collection via LangChain
    vectorstore = Chroma(
        collection_name="argo_profiles",
        embedding_function=embedding_model,
        persist_directory=db_path
    )

    # Example query
    query = "Find profiles with high salinity near equator in March"
    print(f"🔍 Query: {query}")

    # Retrieve top 5 matching documents
    results = vectorstore.similarity_search(query, k=5)

    print("\n🧪 Top Results:")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(doc.page_content)
        print(doc.metadata)

if __name__ == "__main__":
    main()
