import os
from openai import OpenAI
from dotenv import load_dotenv
from app.config import EMBEDDING_KEY
load_dotenv()

embedding_client = OpenAI(
    api_key=EMBEDDING_KEY
)


def create_embeddings(chunks):

    for chunk in chunks:
        response = embedding_client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["text"]
        )

        chunk["embedding"] = response.data[0].embedding

    return chunks
def create_embedding(text):

    response = embedding_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding