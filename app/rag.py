import os

from dotenv import load_dotenv
from openai import OpenAI
from app.config import API_KEY
from app.embeddings import create_embedding
from app.vector_store import search_index


load_dotenv()

chat_client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def answer_question(question, index, chunks):

    query_embedding = create_embedding(question)

    relevant_chunks = search_index(
        index,
        chunks,
        query_embedding,
        k=3
    )

    context = "\n\n".join(
        chunk["text"]
        for chunk in relevant_chunks
    )

    prompt = f"""
Answer the user's question using only the provided context.

Context:
{context}

Question:
{question}

If the answer cannot be found in the context, say that you cannot find the answer in the document.
"""

    response = chat_client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt
    )

    return response.output_text, relevant_chunks