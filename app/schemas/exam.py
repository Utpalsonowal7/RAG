from pydantic import BaseModel, Field


class ExamQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=2, max_length=6)
    correct_answer: int
    explanation: str


class Exam(BaseModel):
    title: str = "Document Exam"
    questions: list[ExamQuestion] = Field(
        min_length=1,
        max_length=50,
    )
