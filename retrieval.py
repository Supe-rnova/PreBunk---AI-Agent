"""Technique retrieval (Track 2): RAG over bias_corpus.py using Chroma.

Every corpus entry becomes one or more chunks (its main text + each extra example).
A message is embedded, the closest chunks are found, and results are grouped
back into techniques, keeping each technique's best score.
"""
import hashlib
import json

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from bias_corpus import BIASES

DB_PATH = "chroma_db"
COLLECTION_NAME = "techniques"
MIN_SCORE = 0.40  # below this, a match is treated as "not found" - tune with test_retrieval.py

BY_ID = {entry["id"]: entry for entry in BIASES}
_collection = None


def _corpus_fingerprint() -> str:
    """Changes whenever bias_corpus.py changes, so the index rebuilds automatically."""
    return hashlib.sha256(json.dumps(BIASES, sort_keys=True).encode()).hexdigest()[:16]


def _build_chunks():
    ids, documents, metadatas = [], [], []
    for entry in BIASES:
        pieces = [entry["text"]] + [f"{entry['name']}: {ex}" for ex in entry.get("extra_examples", [])]
        for i, piece in enumerate(pieces):
            ids.append(f"{entry['id']}-{i}")
            documents.append(piece)
            metadatas.append({"technique_id": entry["id"]})
    return ids, documents, metadatas


def get_collection():
    """Load the vector store, (re)building it if it's missing or the corpus has changed."""
    global _collection
    if _collection is not None:
        return _collection

    client = chromadb.PersistentClient(path=DB_PATH, settings=Settings(anonymized_telemetry=False))
    embedder = DefaultEmbeddingFunction()  # all-MiniLM-L6-v2, runs locally on CPU, no API key
    fingerprint = _corpus_fingerprint()

    collection = None
    try:
        existing = client.get_collection(COLLECTION_NAME, embedding_function=embedder)
        if (existing.metadata or {}).get("fingerprint") == fingerprint:
            collection = existing
        else:
            client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # collection doesn't exist yet

    if collection is None:
        collection = client.create_collection(
            COLLECTION_NAME,
            embedding_function=embedder,
            metadata={"hnsw:space": "cosine", "fingerprint": fingerprint},
        )
        ids, documents, metadatas = _build_chunks()
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
        print(f"[retrieval] Built index: {len(ids)} chunks from {len(BIASES)} techniques")

    _collection = collection
    return collection


def retrieve_techniques(text: str, k: int = 3, min_score: float = MIN_SCORE) -> list[dict]:
    """Return up to k techniques the text most resembles: [{id, name, definition, score}, ...].
    Returns [] if nothing scores at least min_score."""
    if not text or not text.strip():
        return []

    collection = get_collection()
    results = collection.query(query_texts=[text], n_results=min(25, collection.count()))

    best = {}  # technique_id -> best score across its chunks
    for meta, distance in zip(results["metadatas"][0], results["distances"][0]):
        score = 1.0 - distance  # cosine distance -> similarity
        tid = meta["technique_id"]
        best[tid] = max(score, best.get(tid, -1.0))

    matches = []
    for tid, score in sorted(best.items(), key=lambda kv: kv[1], reverse=True):
        if score < min_score or len(matches) >= k:
            break
        entry = BY_ID[tid]
        matches.append({"id": tid, "name": entry["name"], "definition": entry["definition"], "score": round(score, 3)})
    return matches
