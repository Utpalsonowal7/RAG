import json
import re



from app.core.gemini import client
from app.schemas.exam import Exam




async def generate_exam(
    context: str,
    number_of_questions: int = 10,
    difficulty: str = "medium",
) -> Exam:

    prompt = f"""
You are an exam generator.

Create a multiple-choice exam using ONLY the information
provided in the document context below.

Requirements:
- Generate exactly {number_of_questions} questions.
- Difficulty: {difficulty}.
- Every question must have exactly 4 options.
- Only one option can be correct.
- correct_answer must be a zero-based option index.
- Include a short explanation for every answer.
- Do not use information that is not present in the context.
- Do not create duplicate questions.

Return ONLY valid JSON.
Do not use Markdown code fences.

The JSON must have this exact structure:

{{
    "title": "Document Exam",
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": 0,
            "explanation": "Explanation of the correct answer."
        }}
    ]
}}

Document context:
{context}
"""

    response = await client.aio.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "temperature": 0.3,
        },
    )

    raw_response = response.text.strip()

    print("RAW GEMINI RESPONSE:")
    print(raw_response)

    # Remove Markdown JSON code fences if Gemini adds them
    raw_response = re.sub(
        r"^```(?:json)?\s*",
        "",
        raw_response,
        flags=re.IGNORECASE,
    )

    raw_response = re.sub(
        r"\s*```$",
        "",
        raw_response,
    )

    raw_response = raw_response.strip()

    print("CLEANED GEMINI RESPONSE:")
    print(raw_response)

    # Convert JSON string into Python dictionary
    data = json.loads(raw_response)

    # Gemini sometimes returns:
    #
    # {
    #     "exam": [...]
    # }
    #
    # while our Pydantic schema expects:
    #
    # {
    #     "questions": [...]
    # }
    if "exam" in data and "questions" not in data:
        data["questions"] = data.pop("exam")

    # Validate the normalized data with Pydantic
    return Exam.model_validate(data)
