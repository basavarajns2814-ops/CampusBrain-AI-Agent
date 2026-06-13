from pypdf import PdfReader
import streamlit as st
import chromadb
import uuid

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

    try:

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
        # UUID IDS
        # =========================

        ids = [
            str(uuid.uuid4())
            for _ in chunks
        ]

        # =========================
        # METADATA
        # =========================

        metadatas = [
            {
                "source": uploaded_file.name,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]

        # =========================
        # STORE IN CHROMADB
        # =========================

        collection.add(
            documents=chunks,
            embeddings=embeddings.tolist(),
            ids=ids,
            metadatas=metadatas
        )

        # =========================
        # SESSION STATE
        # =========================

        st.session_state.pdf_uploaded = True

        if "uploaded_pdfs" not in st.session_state:
            st.session_state.uploaded_pdfs = []

        if uploaded_file.name not in st.session_state.uploaded_pdfs:
            st.session_state.uploaded_pdfs.append(
                uploaded_file.name
            )

        st.session_state.chunk_count = len(
            chunks
        )

        return len(chunks)

    except Exception as e:

        st.error(
            f"PDF Processing Error: {str(e)}"
        )

        return 0


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
        n_results=5,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved_chunks = results[
        "documents"
    ][0]

    distances = results[
        "distances"
    ][0]

    metadata = results[
        "metadatas"
    ][0]

    context = "\n".join(
        retrieved_chunks
    )

    return (
        context,
        distances,
        metadata
    )