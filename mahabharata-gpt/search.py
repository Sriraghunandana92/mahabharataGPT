import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index("mahabharata.index")

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


def search(question, k=5):
    q_vec = model.encode([question], normalize_embeddings=True)
    q_vec = np.array(q_vec, dtype="float32")

    scores, positions = index.search(q_vec, k)

    results = []
    for score, pos in zip(scores[0], positions[0]):
        chunk = chunks[pos]
        results.append({
            "score": float(score),
            "citation": chunk["citation"],
            "text": chunk["text"],
        })
    return results


if __name__ == "__main__":
    question = input("Ask a question: ")
    for r in search(question):
        print("\n---")
        print(r["citation"], "| score:", round(r["score"], 3))
        print(r["text"][:400])