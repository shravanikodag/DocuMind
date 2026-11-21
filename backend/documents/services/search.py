
import numpy as np

from documents.models import DocumentChunk
from documents.services.embeddings import EmbeddingService


def search_document(document, question, top_k=3):

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    # Get saved text chunks
    chunks = list(
        DocumentChunk.objects.filter(document=document)
    )

    if not chunks:
        return []

    # Generate embeddings
    embedding_service = EmbeddingService()

    texts = [chunk.content for chunk in chunks]

    chunk_vectors = embedding_service.generate_embeddings(texts)
    question_vector = embedding_service.generate_embeddings([question])[0]

    # Calculate similarity
    scores = np.dot(chunk_vectors, question_vector)

    # Get the best matching chunks
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for i in top_indices:
        results.append({
            "text": chunks[i].content,
            "page": chunks[i].page_number,
            "score": round(float(scores[i]), 3)
        })

    return results
