from app.core.gemini import client

async def generate_answer(question: str, context: str):
    prompt = f"""
You are a helpful assistant answering questions based on the provided context.

Use only the information from the context to answer the question.
If the answer is not present in the context, say:
"I couldn't find the answer in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "temperature": 0.2,
        },
    )

    return response.text
