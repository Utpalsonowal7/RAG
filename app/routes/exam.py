from fastapi import APIRouter

from app.schemas.exam import Exam
from app.services.emb import create_embedding
from app.services.vector_store import search
from app.services.exam import generate_exam

router = APIRouter(prefix="/exam")


@router.post("/generate", response_model=Exam)
async def create_exam(
    number_of_questions: int = 10,
    difficulty: str = "medium",
):
    query = "Generate an exam covering the important concepts in this document."

    query_embedding = await create_embedding(query)

    results = search(
        query_embedding,
        top_k=10,
    )

    if not results:
        return {
            "title": "No Exam Available",
            "questions": [],
        }

    context = "\n\n".join(result["text"] for result in results)

    exam = await generate_exam(
        context=context,
        number_of_questions=number_of_questions,
        difficulty=difficulty,
    )

    return exam
