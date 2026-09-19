import streamlit as st

from app.pdf_loader import load_pdf
from app.chunker import chunker
from app.embeddings import create_embeddings
from app.vector_store import create_index
from app.rag import answer_question


st.title("PDF RAG Assistant")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


if uploaded_file:

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Processing PDF..."):

        pages = load_pdf("temp.pdf")

        chunks = chunker(pages)

        chunks = create_embeddings(chunks)

        index = create_index(chunks)

    st.success("PDF processed successfully!")

    question = st.text_input(
        "Ask a question about your PDF"
    )

    if question:

        with st.spinner("Thinking..."):

            answer = answer_question(
                question,
                index,
                chunks
            )

        st.write("### Answer")
        st.write(answer)