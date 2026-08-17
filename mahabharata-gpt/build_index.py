import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from chunker import make_chunks

MODEL_NAME = "all-MiniLM-L6-v2"

print("Starting...")

def main():
    chunks = make_chunks()
    print("Chunks to embed:", len(chunks))

    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    texts = [c["text"] for c in chunks]

    print("Embedding... (this takes a few minutes)")
    vectors = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    vectors = np.array(vectors, dtype="float32")
    print("Vector shape:", vectors.shape)

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    print("Vectors in index:", index.ntotal)

    faiss.write_index(index, "mahabharata.index")

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False)

    print("Saved mahabharata.index and chunks.json")


if __name__ == "__main__":
    main()