from google import genai
from app.config import GEMI

client = genai.Client(api_key=GEMI)


async def create_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    return response.embeddings[0].values


async def create_embeddings(chunks: list[str]):
    embeddings = []

    for chunk in chunks:
        embedding = await create_embedding(chunk)
        embeddings.append(embedding)

    return embeddings
