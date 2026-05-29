from pypdf import PdfReader
import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer

# =========================
# CHROMADB CLIENT
# =========================

client = chromadb.PersistentClient(
    path="./chroma_db"
)

# =========================
# COLLECTION
# =========================

collection = client.get_or_create_collection(
    name="pdf_chunks"
)

# =========================
# EMBEDDING MODEL
# =========================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =========================
# PDF PROCESSING FUNCTION
# =========================

def process_pdf(uploaded_file):

    global collection

    # Reset previous PDF vectors
    try:
        client.delete_collection("pdf_chunks")
    except:
        pass

    collection = client.get_or_create_collection(
        name="pdf_chunks"
    )

    # Read PDF
    reader = PdfReader(uploaded_file)

    raw_text = ""
    chunks = []

    # =========================
    # TEXT EXTRACTION
    # =========================

    for page in reader.pages:

        text = page.extract_text()

        if text:
            raw_text += text

    # =========================
    # CHUNKING
    # =========================

    chunk_size = 500
    overlap = 100

    start = 0

    while start < len(raw_text):

        end = start + chunk_size

        chunk = raw_text[start:end]

        chunks.append(chunk)

        start = end - overlap

    # =========================
    # EMBEDDINGS
    # =========================

    embeddings = embedding_model.encode(
        chunks
    )

    # =========================
    # IDS
    # =========================

    ids = []

    for i in range(len(chunks)):

        ids.append(
            f"chunk_{i}"
        )

    # =========================
    # STORE IN CHROMADB
    # =========================

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids
    )

    # =========================
    # SESSION STATE
    # =========================

    st.session_state.pdf_uploaded = True

    st.session_state.chunk_count = len(
        chunks
    )

    return len(chunks)

# =========================
# RETRIEVAL FUNCTION
# =========================

def retrieve_context(question):

    query_embedding = embedding_model.encode(
        question
    )

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=3
    )

    retrieved_chunks = results[
        "documents"
    ][0]

    context = "\n".join(
        retrieved_chunks
    )

    return context