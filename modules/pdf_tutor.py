from pypdf import PdfReader
import streamlit as st


def pdf_tutor_ui():

    st.write("Upload a PDF to get started")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf"
    )

    # Process only if PDF is uploaded
    if uploaded_file is not None:

        # Read PDF
        reader = PdfReader(uploaded_file)

        # Store extracted text
        raw_text = ""

        # Store chunks
        chunks = []

        # Extract text page by page
        for page in reader.pages:

            text = page.extract_text()

            # Avoid None errors
            if text:
                raw_text += text

        # Chunking settings
        chunk_size = 500
        overlap = 100

        # Starting position
        start = 0

        # Generate chunks
        while start < len(raw_text):

            # Define chunk window
            end = start + chunk_size

            # Extract chunk
            chunk = raw_text[start:end]

            # Store chunk
            chunks.append(chunk)

            # Move window with overlap
            start = end - overlap

        # Store in session state
        st.session_state.raw_text = raw_text
        st.session_state.chunks = chunks

        # Debugging (temporary)
        st.write(f"Total Chunks Created: {len(chunks)}")
        

        # Success message
        st.success("PDF uploaded and processed successfully!")