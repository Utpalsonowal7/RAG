import asyncio

from app.services.emb import create_embedding


async def main():
    text = "Bachelor of Computer Applications is a program in computer science and software development."

    vector = await create_embedding(text)

    print("Vector length:", len(vector))
    print("First 10 values:", vector[:10])


asyncio.run(main())
