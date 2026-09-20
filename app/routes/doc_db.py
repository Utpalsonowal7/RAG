from pathlib import Path
import json

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse

from app.services.doc import extract_text
from app.services.chunker import chunk_text
from app.services.emb import create_embeddings, create_embedding
from app.services.llm import generate_answer_stream
from app.services.vector_store_db import (
    save_document,
    search_documents,
)

router = APIRouter(prefix="/doc-db")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        buffer.write(await file.read())

    text = extract_text(file_path)
    chunks = chunk_text(text)

    print("Total chunks:", len(chunks))

    embeddings = await create_embeddings(chunks)

    document_id = await save_document(
        filename=file.filename,
        chunks=chunks,
        embeddings=embeddings,
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "total_characters": len(text),
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings),
        "embedding_dimension": len(embeddings[0]),
    }


@router.get("/ask")
async def ask_question(query: str):
    query_embedding = await create_embedding(query)

    results = await search_documents(
        query_embedding=query_embedding,
        top_k=3,
        threshold=0.6,
    )

    if not results:

        async def no_results():
            yield "event: answer\n"
            yield (
                'data: {"text":"I couldn\'t find the answer '
                'in the provided document."}\n\n'
            )

            yield "event: done\n"
            yield "data: {}\n\n"

        return StreamingResponse(
            no_results(),
            media_type="text/event-stream",
        )

    context = "\n\n".join(result["text"] for result in results)

    async def event_stream():

        yield "event: sources\n"
        yield f"data: {json.dumps(results)}\n\n"

        async for text in generate_answer_stream(
            question=query,
            context=context,
        ):
            yield "event: token\n"
            yield f"data: {json.dumps({'text': text})}\n\n"

        yield "event: done\n"
        yield "data: {}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
