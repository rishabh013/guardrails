"""
RAG pipeline: build a FAISS vector store from HR documents and retrieve 
relevant chunks.
Using FAISS (no telemetry dependencies) instead of ChromaDB.
"""


import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from src.hr_docs import HR_DOCUMENTS

EMBED_MODEL   = "text-embedding-3-small"
CHUNK_SIZE    = 500
CHUNK_OVERLAP = 100



def _make_documents():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    docs = []
    for item in HR_DOCUMENTS:
        chunks = splitter.create_documents(
            texts=[item["content"]],
            metadatas=[{"source": item["title"]}],
        )
        docs.extend(chunks)
    return docs



@st.cache_resource(show_spinner="Building HR policy index…")
def build_vectorstore(openai_api_key: str):
    embeddings = OpenAIEmbeddings(model=EMBED_MODEL, api_key=openai_api_key)
    docs = _make_documents()
    vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
    return vectorstore


def retrieve(query: str, vectorstore, k: int = 3):
    """Return top-k chunks with relevance scores."""
    results = vectorstore.similarity_search_with_relevance_scores(query, k=k)
    return [
        {
            "source": doc.metadata.get("source", "Unknown"),
            "content": doc.page_content,
            "score": round(score, 3),
        }
        for doc, score in results
    ]
