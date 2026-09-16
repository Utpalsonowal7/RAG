import re


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    text = re.sub(r"\s+", " ", text).strip()

    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            overlap_text = current_chunk[-overlap:] if current_chunk else ""

            current_chunk = overlap_text + " " + sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
