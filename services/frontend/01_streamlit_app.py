# services/frontend/01_streamlit_app.py

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load the Chroma vector store
@st.cache_resource
def load_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vectorstore = Chroma(persist_directory="db", embedding_function=embedding_model, collection_name="argo_profiles")
    return vectorstore

vectorstore = load_vectorstore()

st.set_page_config(layout="wide")
st.title("🌊 FloatChat Explorer — Ask the Ocean")

# Query box
query = st.text_input("Ask something about the ocean profiles...", "Find warm, salty water in the Indian Ocean")

if query:
    st.markdown("### 🔍 Top Matching Profiles")
    results = vectorstore.similarity_search_with_score(query, k=5)

    # Collect metadata
    data = []
    for doc, score in results:
        meta = doc.metadata
        meta["score"] = round(score, 3)
        data.append(meta)

    df = pd.DataFrame(data)
    st.dataframe(df[["date_time", "latitude", "longitude", "temperature_mean", "salinity_mean", "score"]])

    # Show on map
    st.markdown("### 🗺️ Map View")
    if not df.empty:
        m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=3)
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=(row.latitude, row.longitude),
                radius=6,
                color="blue",
                fill=True,
                fill_color="cyan",
                popup=(
                    f"Date: {row.date_time}<br>"
                    f"Temp: {row.temperature_mean:.2f}<br>"
                    f"Salinity: {row.salinity_mean:.2f}"
                )
            ).add_to(m)

        st_folium(m, width=700, height=500)
