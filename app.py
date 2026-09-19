import streamlit as st

from app.pdf_loader import load_pdf
from app.chunker import chunker
from app.embeddings import create_embeddings
from app.vector_store import create_index
from app.rag import answer_question


st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📄",
    layout="wide"
)


# ---------- SESSION STATE ----------

if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------- SIDEBAR ----------

with st.sidebar:

    st.title("📄 PDF RAG")

    st.caption("Ask questions about your documents using semantic search.")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_file:

        if uploaded_file.name != st.session_state.file_name:

            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Processing document..."):

                pages = load_pdf("temp.pdf")

                chunks = chunker(pages)

                chunks = create_embeddings(chunks)

                index = create_index(chunks)

                st.session_state.index = index
                st.session_state.chunks = chunks
                st.session_state.file_name = uploaded_file.name
                st.session_state.messages = []

            st.success("Document ready!")

    if st.session_state.index is not None:

        st.divider()

        st.subheader("Document")

        st.write(f"**{st.session_state.file_name}**")

        st.caption(
            f"{len(st.session_state.chunks)} chunks indexed"
        )

        st.divider()

        st.caption("RAG Pipeline")

        st.write("✓ PDF extraction")
        st.write("✓ Chunking")
        st.write("✓ Embeddings")
        st.write("✓ FAISS retrieval")


# ---------- MAIN AREA ----------

st.title("Ask your document")

st.caption(
    "Upload a PDF and ask questions using its contents."
)


if st.session_state.index is None:

    st.info(
        "Upload a PDF from the sidebar to start asking questions."
    )


else:

    # Display previous messages

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


    question = st.chat_input(
        "Ask something about your document..."
    )


    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Searching document..."):

                answer = answer_question(
                    question,
                    st.session_state.index,
                    st.session_state.chunks
                )

            st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })