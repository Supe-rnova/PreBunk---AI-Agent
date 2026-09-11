"""Technique retrieval (Track 2): hybrid RAG over bias_corpus.py using Chroma.

Score = semantic similarity + a boost for each corpus "marker" phrase found in the message.
- Semantic: every corpus entry becomes chunks (main text + each extra example), embedded
  with all-MiniLM-L6-v2; each technique keeps its best-matching chunk's cosine similarity.
- Lexical: marker phrases (e.g. "forwarded as received") catch tell-tale wording that
  a small embedding model misses. Matched phrases are returned, so every match is traceable.
"""
import hashlib
import json
import re

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from bias_corpus import BIASES

DB_PATH = "chroma_db"
COLLECTION_NAME = "techniques"
MIN_SCORE = 0.40      # below this, a match is treated as "not found" - tune with test_retrieval.py
MARKER_BOOST = 0.20   # added per marker phrase found in the message
MAX_MARKER_HITS = 2   # at most +0.40 from markers

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


def _normalize(text: str) -> str:
    # phones often use curly apostrophes; make them match the corpus
    return text.lower().replace("\u2019", "'").replace("\u2018", "'")


def _marker_found(marker: str, lowered_text: str) -> bool:
    m = _normalize(marker)
    pattern = re.escape(m)
    if m[:1].isalnum():
        pattern = r"\b" + pattern   # whole words only, so "evil" doesn't match "medieval"
    if m[-1:].isalnum():
        pattern = pattern + r"\b"
    return re.search(pattern, lowered_text) is not None


def retrieve_techniques(text: str, k: int = 3, min_score: float = MIN_SCORE) -> list[dict]:
    """Return up to k techniques the text most resembles:
    [{id, name, definition, score, matched_markers}, ...]. Returns [] if nothing reaches min_score."""
    if not text or not text.strip():
        return []

    collection = get_collection()
    results = collection.query(query_texts=[text], n_results=collection.count())

    semantic = {}  # technique_id -> best cosine similarity across its chunks
    for meta, distance in zip(results["metadatas"][0], results["distances"][0]):
        tid = meta["technique_id"]
        semantic[tid] = max(1.0 - distance, semantic.get(tid, -1.0))

    lowered = _normalize(text)
    scored = []
    for tid, entry in BY_ID.items():
        hits = [m for m in entry.get("markers", []) if _marker_found(m, lowered)]
        score = semantic.get(tid, 0.0) + MARKER_BOOST * min(len(hits), MAX_MARKER_HITS)
        scored.append((min(score, 1.0), tid, hits))
    scored.sort(key=lambda item: item[0], reverse=True)

    matches = []
    for score, tid, hits in scored:
        if score < min_score or len(matches) >= k:
            break
        entry = BY_ID[tid]
        matches.append({"id": tid, "name": entry["name"], "definition": entry["definition"],
                        "score": round(score, 3), "matched_markers": hits})
    return matches
