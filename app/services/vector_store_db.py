from sqlalchemy import select

from app.db.db import sessionLocal
from app.db.models import Document, DocumentChunk


async def save_document(
    filename: str,
    chunks: list[str],
    embeddings: list[list[float]],
):
    async with sessionLocal() as session:
        document = Document(
            filename=filename,
        )

        session.add(document)

        await session.flush()

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            document_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )

            session.add(document_chunk)

        await session.commit()

        return document.id


async def search_documents(
    document_id: int,
    query_embedding: list[float],
    top_k: int = 3,
    threshold: float = 0.6,
):
    async with sessionLocal() as session:

        distance = DocumentChunk.embedding.cosine_distance(query_embedding)

        statement = (
            select(
                DocumentChunk.content,
                distance.label("distance"),
            )
            .where(DocumentChunk.document_id == document_id)
            .order_by(distance)
            .limit(top_k)
        )

        result = await session.execute(statement)

        rows = result.all()

        results = []

        for row in rows:
            similarity = 1 - row.distance

            if similarity >= threshold:
                results.append(
                    {
                        "text": row.content,
                        "similarity": float(similarity),
                    }
                )

        return results
