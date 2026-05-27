from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

# =========================
# CHROMADB CLIENT
# =========================

client = chromadb.Client()

# =========================
# CREATE / GET COLLECTION
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

    # Read PDF
    reader = PdfReader(uploaded_file)

    # Store extracted text
    raw_text = ""

    # Store chunks
    chunks = []

    # =========================
    # TEXT EXTRACTION
    # =========================

    for page in reader.pages:

        text = page.extract_text()

        # Avoid None issues
        if text:
            raw_text += text

    # =========================
    # CHUNKING
    # =========================

    chunk_size = 500
    overlap = 100

    start = 0

    while start < len(raw_text):

        # Define chunk window
        end = start + chunk_size

        # Extract chunk
        chunk = raw_text[start:end]

        # Store chunk
        chunks.append(chunk)

        # Move window with overlap
        start = end - overlap

    # =========================
    # GENERATE EMBEDDINGS
    # =========================

    embeddings = embedding_model.encode(chunks)

    # =========================
    # CREATE IDS
    # =========================

    ids = []

    for i in range(len(chunks)):
        ids.append(f"chunk_{i}")

    # =========================
    # STORE IN CHROMADB
    # =========================

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids
    )

    # Return useful info
    return len(chunks)

# =========================
# RETRIEVAL FUNCTION
# =========================

def retrieve_context(question):

    # Convert question to embedding
    query_embedding = embedding_model.encode(
        question
    )

    # Search nearest chunks
    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=3
    )

    # Extract retrieved chunks
    retrieved_chunks = results["documents"][0]

    # Combine into single context
    context = "\n".join(retrieved_chunks)

    return context