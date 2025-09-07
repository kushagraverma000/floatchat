# scripts/03_generate_embeddings.py

import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import chromadb
from chromadb.config import Settings
import os

def main():
    # Load processed CSV
    df = pd.read_csv("data/processed/profiles_2024.csv")

    # Convert each row to descriptive text
    def profile_to_text(row):
        return (f"Profile at lat {row.latitude:.2f}, lon {row.longitude:.2f}, "
                f"date {row.date_time}, mean temp {row.temperature_mean:.2f}, "
                f"mean salinity {row.salinity_mean:.2f}")

    df['text'] = df.apply(profile_to_text, axis=1)

    # Load sentence-transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings
    print("Generating embeddings...")
    texts = df['text'].tolist()
    embeddings = model.encode(texts, show_progress_bar=True)

    # Prepare ChromaDB client (Persistent)
    db_path = os.path.join(os.getcwd(), "db")  # stores on disk
    client = chromadb.PersistentClient(path=db_path)

    # Create or recreate collection
    collection_name = "argo_profiles"
    if collection_name in [col.name for col in client.list_collections()]:
        client.delete_collection(collection_name)
    collection = client.create_collection(name=collection_name)

    print("Adding embeddings to ChromaDB...")

    # Prepare data
    ids = [str(i) for i in range(len(df))]
    metadatas = df.drop(columns=['text']).to_dict(orient='records')
    documents = texts
    BATCH_SIZE = 5000

    for start_idx in tqdm(range(0, len(ids), BATCH_SIZE), desc="Batches"):
        end_idx = min(start_idx + BATCH_SIZE, len(ids))
        collection.add(
            ids=ids[start_idx:end_idx],
            embeddings=embeddings[start_idx:end_idx].tolist(),
            metadatas=metadatas[start_idx:end_idx],
            documents=documents[start_idx:end_idx],
        )

    print(f"\n✅ Done! Stored {len(ids)} embeddings in ChromaDB collection '{collection_name}'.")

if __name__ == "__main__":
    main()
