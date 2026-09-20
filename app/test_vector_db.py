import asyncio

from app.services.emb import create_embedding
from app.services.vector_store_db import search_documents


async def main():

    query = "What is FastAPI?"

    query_embedding = await create_embedding(query)

    results = await search_documents(
        query_embedding=query_embedding,
        top_k=3,
        threshold=0.0,
    )

    for result in results:
        print("\nSimilarity:", result["similarity"])
        print("Text:", result["text"])


if __name__ == "__main__":
    asyncio.run(main())
