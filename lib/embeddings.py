"""Local vector embeddings and similarity helpers for SecondSelf."""

import hashlib
import pickle
import re
from typing import Any, Callable, Dict, Iterable, List

import numpy as np

from lib.storage import DATA_DIR, EMBEDDINGS_FILE


_EMBEDDING_MODEL = None
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384


def load_model():
    """Load the cached SentenceTransformer model, falling back locally if unavailable."""
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            _EMBEDDING_MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME)
        except Exception as exc:
            print(f"Warning: SentenceTransformer unavailable; using stable fallback: {exc}")
            _EMBEDDING_MODEL = "FALLBACK"
    return _EMBEDDING_MODEL


def embed_text(text: str) -> List[float]:
    """Compute a 384-dimensional dense vector for text."""
    text_clean = (text or "").strip()
    if not text_clean:
        return [0.0] * EMBEDDING_DIMENSION

    model = load_model()
    if model != "FALLBACK" and hasattr(model, "encode"):
        vector = model.encode(text_clean)
        return vector.tolist()

    # Python's built-in hash() is salted per process. Use a stable digest
    # for persisted fallback vectors instead.
    vector = np.zeros(EMBEDDING_DIMENSION, dtype=float)
    for word in re.findall(r"[\w'-]+", text_clean.lower()):
        digest = hashlib.blake2b(word.encode("utf-8"), digest_size=8).digest()
        index = int.from_bytes(digest, "big") % EMBEDDING_DIMENSION
        vector[index] += 1.0
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector /= norm
    return vector.tolist()


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Return cosine similarity, or zero for empty/incompatible vectors."""
    a = np.asarray(vec_a, dtype=float)
    b = np.asarray(vec_b, dtype=float)
    if a.shape != b.shape or a.size == 0:
        return 0.0
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def embedding_fingerprint(text: str) -> str:
    return hashlib.sha256((text or "").strip().encode("utf-8")).hexdigest()


def _load_payload() -> Any:
    if not EMBEDDINGS_FILE.exists():
        return {}
    try:
        with open(EMBEDDINGS_FILE, "rb") as handle:
            return pickle.load(handle)
    except Exception as exc:
        print(f"Warning: Could not read embedding cache: {exc}")
        return {}


def load_embeddings() -> Dict[str, List[float]]:
    """Load vectors, including compatibility with the old plain-dict format."""
    payload = _load_payload()
    vectors = payload.get("vectors", {}) if isinstance(payload, dict) and "vectors" in payload else payload
    return vectors if isinstance(vectors, dict) else {}


def load_embedding_fingerprints() -> Dict[str, str]:
    payload = _load_payload()
    if not isinstance(payload, dict):
        return {}
    return {str(key): str(value) for key, value in payload.get("fingerprints", {}).items()}


def save_embeddings(embeddings_dict: Dict[str, List[float]], fingerprints: Dict[str, str] | None = None) -> None:
    """Persist vectors and content fingerprints atomically."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "format_version": 2,
        "model": EMBEDDING_MODEL_NAME,
        "dimension": EMBEDDING_DIMENSION,
        "fingerprints": fingerprints or {},
        "vectors": embeddings_dict,
    }
    temp_path = EMBEDDINGS_FILE.with_name(f".{EMBEDDINGS_FILE.name}.{hashlib.sha1(str(id(payload)).encode()).hexdigest()[:8]}.tmp")
    try:
        with open(temp_path, "wb") as handle:
            pickle.dump(payload, handle)
            handle.flush()
        temp_path.replace(EMBEDDINGS_FILE)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def ensure_embeddings(notes: Iterable[Any], text_for_note: Callable[[Any], str] | None = None) -> Dict[str, List[float]]:
    """Return a complete cache, refreshing vectors whose note content changed."""
    note_list = list(notes)
    text_for_note = text_for_note or (lambda note: f"{note.summary}\n{note.body}")
    vectors = load_embeddings()
    fingerprints = load_embedding_fingerprints()
    current_ids = set()
    changed = False

    for note in note_list:
        text = text_for_note(note)
        current_ids.add(note.id)
        fingerprint = embedding_fingerprint(text)
        vector = vectors.get(note.id)
        if not vector or fingerprints.get(note.id) != fingerprint or len(vector) != EMBEDDING_DIMENSION:
            vectors[note.id] = embed_text(text)
            fingerprints[note.id] = fingerprint
            changed = True

    for stale_id in set(vectors) - current_ids:
        vectors.pop(stale_id, None)
        fingerprints.pop(stale_id, None)
        changed = True

    if changed or not EMBEDDINGS_FILE.exists():
        save_embeddings(vectors, fingerprints)
    return vectors
