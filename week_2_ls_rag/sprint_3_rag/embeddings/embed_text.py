from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_text(text: str):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)

    return response.data[0].embedding


def build_embeddings(chunks):
    vector_db = []

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk["text"])

        vector_db.append(
            {
                "id": i,
                "embedding": embedding,
                "text": chunk["text"],
                "source": chunk["source"],
                "header": chunk.get("header"),
            }
        )

    return vector_db
