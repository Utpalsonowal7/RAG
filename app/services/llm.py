from app.core.gemini import client


async def generate_answer_stream(question: str, context: str):
    prompt = f"""
You are a helpful assistant answering questions based on the provided context.

Use only the information from the context to answer the question.
And also when you find the answer try to explain from the context a boardly according to the user if they say short give short answer and if say explain then a long response and also don't say based on the provied conext.
If the answer is not present in the context, say:
"I couldn't find the answer in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = await client.aio.models.generate_content_stream(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "temperature": 0.2,
        },
    )

    async for chunk in response:
        if chunk.text:
            yield chunk.text
