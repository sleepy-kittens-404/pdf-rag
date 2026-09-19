import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

embedding_client = OpenAI(
    api_key=os.getenv("EMBEDDING_KEY")
)


def create_embeddings(chunks):

    for chunk in chunks:
        response = embedding_client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["text"]
        )

        chunk["embedding"] = response.data[0].embedding

    return chunks