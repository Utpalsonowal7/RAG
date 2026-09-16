from fastapi import APIRouter, UploadFile, File
from pathlib import Path

from app.services.doc import extract_text
from app.services.chunker import chunk_text
from app.services.emb import create_embeddings, create_embedding
from app.services.vector_store import add_documents, search

router = APIRouter(prefix="/doc")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        buffer.write(await file.read())

    text = extract_text(file_path)

    chunks = chunk_text(text)

    embeddings = await create_embeddings(chunks)
    add_documents(chunks, embeddings)

    return {
        "filename": file.filename,
        "total_characters": len(text),
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings),
        "embedding_dimension": len(embeddings[0]),
    }


@router.get("/search")
async def search_documents(query: str):
    query_embedding = await create_embedding(query)

    results = search(query_embedding)

    return {
        "query": query,
        "results": results,
    }
