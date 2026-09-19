from app.pdf_loader import load_pdf
from app.chunker import chunker
from app.embeddings import create_embeddings
from app.vector_store import create_index
from app.rag import answer_question


PDF_PATH = "data/sample.pdf"


pages = load_pdf(PDF_PATH)

chunks = chunker(pages)

chunks = create_embeddings(chunks)

index = create_index(chunks)

print("RAG system ready!")

while True:

    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    answer = answer_question(
        question,
        index,
        chunks
    )

    print("\nAnswer:")
    print(answer)