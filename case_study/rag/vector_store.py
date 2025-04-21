import json
import numpy as np
from nomic import embed
from case_study.rag.config import settings

VECTOR_STORE_FILEPATH = "data/{doc}_vector_store.json"


def cosine_similarity(query_vector, vectors):
    """Calculates the cosine similarity between a query vector and a list of vectors."""
    query_vector = np.array(query_vector)
    vectors = np.array(vectors)
    return np.dot(vectors, query_vector) / (
        np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_vector)
    )


class VectorStore:
    def __init__(self, doc_type="contracts"):
        self.filepath = VECTOR_STORE_FILEPATH.format(doc=doc_type)
        self.store = []

    def add(self, items):
        self.store.extend(items)

    def save(self):
        file_path = self.filepath
        with open(file_path, "w") as f:
            json.dump(self.store, f)

    def load(self):
        file_path = self.filepath
        with open(file_path, "r") as f:
            self.store = json.load(f)

    def query(self, vector, top_k=10):
        vectors = [item["vector"] for item in self.store]
        similarities = cosine_similarity(vector, vectors)
        top_k_indices = np.argsort(similarities)[-top_k:][::-1]
        return [{**self.store[i], "score": similarities[i]} for i in top_k_indices]

    def similarity_search(self, user_query, top_k=5):
        # Embed the user's question
        embed_res = embed.text(
            texts=[user_query],
            model="nomic-embed-text-v1.5",
            task_type="search_query",
            inference_mode=settings.NOMIC_INFERENCE_MODE,
        )
        query_vector = embed_res["embeddings"][0]

        # Find the most relevant chunks in our vector store using semantic search
        return self.query(query_vector, top_k)
