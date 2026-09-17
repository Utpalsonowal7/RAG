import numpy as np

documents = []


def add_documents(chunks, embeddings):
    for chunk, embedding in zip(chunks, embeddings):
        documents.append(
            {
                "text": chunk,
                "embedding": np.array(embedding),
            }
        )


def cosine_similarity(vector_a, vector_b):
    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )


def search(query_embedding, top_k=3, threshold=0.6):
    query_embedding = np.array(query_embedding)
    results = []

    for document in documents:
        similarity = cosine_similarity(
            query_embedding,
            document["embedding"],
        )

        if similarity >= threshold:
            results.append(
                {
                    "text": document["text"],
                    "similarity": float(similarity),
                }
            )

    results.sort(
        key=lambda result: result["similarity"],
        reverse=True,
    )

    return results[:top_k]
