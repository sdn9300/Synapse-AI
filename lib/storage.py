"""Filesystem, storage, hashing, and JSON IO helpers for SecondSelf."""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

from lib.models import CaptureMeta, WikiNote


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "raw"
WIKI_DIR = PROJECT_ROOT / "wiki"
DATA_DIR = PROJECT_ROOT / "data"
STATIC_DIR = PROJECT_ROOT / "static"
INDEX_FILE = DATA_DIR / "index.json"
GRAPH_FILE = DATA_DIR / "graph.json"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.pkl"
PARA_CATEGORIES = ("Projects", "Areas", "Resources", "Archives")


def _atomic_write(path: Path, data: str | bytes, *, binary: bool = False) -> None:
    """Write a file atomically so interrupted maintenance cannot leave partial state."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        mode = "wb" if binary else "w"
        kwargs = {} if binary else {"encoding": "utf-8"}
        with open(temp_path, mode, **kwargs) as handle:
            handle.write(data)
            handle.flush()
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def ensure_directories() -> None:
    """Ensure all required project directories exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    for category in PARA_CATEGORIES:
        (WIKI_DIR / category).mkdir(parents=True, exist_ok=True)


def generate_capture_id() -> str:
    """Generate a capture ID in the format YYYY-MM-DD_{uuid8}."""
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"{date_str}_{uuid.uuid4().hex[:8]}"


def content_hash(data: str | bytes) -> str:
    """Compute a SHA-256 hash of string or byte content."""
    data_bytes = data.encode("utf-8") if isinstance(data, str) else data
    return hashlib.sha256(data_bytes).hexdigest()


def write_raw_capture(meta: CaptureMeta, content: str | bytes) -> Path:
    """Write one raw capture without overwriting an existing capture ID."""
    ensure_directories()
    folder = RAW_DIR / meta.id
    if folder.exists():
        raise FileExistsError(f"Raw capture already exists: {meta.id}")
    folder.mkdir(parents=True, exist_ok=False)

    meta_dict = {
        "id": meta.id,
        "timestamp": meta.timestamp,
        "type": meta.type,
        "source": meta.source,
        "original_filename": meta.original_filename,
        "content_hash": meta.content_hash,
    }
    _atomic_write(folder / "meta.json", json.dumps(meta_dict, indent=2) + "\n")

    if meta.original_filename:
        extension = Path(meta.original_filename).suffix.lstrip(".")
        content_filename = f"content.{extension}" if extension else "content.txt"
    elif meta.type == "link":
        content_filename = "content.url"
    else:
        content_filename = "content.md"
    content_path = folder / content_filename
    _atomic_write(content_path, content if isinstance(content, str) else content, binary=not isinstance(content, str))
    return folder


def read_raw_captures() -> List[Tuple[CaptureMeta, str | bytes, Path]]:
    """Read valid captured items from raw/; skip and report corrupt items."""
    ensure_directories()
    results: List[Tuple[CaptureMeta, str | bytes, Path]] = []
    for item in sorted(RAW_DIR.iterdir()):
        if not item.is_dir():
            continue
        meta_path = item / "meta.json"
        if not meta_path.exists():
            continue
        try:
            with open(meta_path, "r", encoding="utf-8") as handle:
                meta = CaptureMeta(**json.load(handle))
            content_files = sorted(f for f in item.iterdir() if f.name != "meta.json" and f.is_file())
            if not content_files:
                print(f"Warning: Raw capture '{item.name}' has no content file; skipped.")
                continue
            content_path = content_files[0]
            try:
                with open(content_path, "r", encoding="utf-8") as handle:
                    content: str | bytes = handle.read()
            except UnicodeDecodeError:
                with open(content_path, "rb") as handle:
                    content = handle.read()
            results.append((meta, content, content_path))
        except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
            print(f"Warning: Failed to read raw capture '{item.name}': {exc}")
    return results


def find_duplicate_capture(data: str | bytes) -> CaptureMeta | None:
    """Find an existing raw capture with identical content, if present."""
    digest = content_hash(data)
    for meta, _, _ in read_raw_captures():
        if meta.content_hash == digest:
            return meta
    return None


def _default_index() -> Dict[str, Any]:
    return {
        "raw_processed": {},
        "embeddings_version": "all-MiniLM-L6-v2",
        "last_graph_build": None,
    }


def load_index() -> Dict[str, Any]:
    """Load processing state, tolerating a missing or malformed state file."""
    ensure_directories()
    if not INDEX_FILE.exists():
        state = _default_index()
        save_index(state)
        return state
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Warning: Could not read {INDEX_FILE.name}: {exc}. Rebuilding in memory.")
        return _default_index()
    data.setdefault("raw_processed", {})
    data.setdefault("embeddings_version", "all-MiniLM-L6-v2")
    data.setdefault("last_graph_build", None)
    return data


def save_index(index_data: Dict[str, Any]) -> None:
    """Persist processing state atomically."""
    ensure_directories()
    _atomic_write(INDEX_FILE, json.dumps(index_data, indent=2) + "\n")


def write_wiki_note(note: WikiNote) -> Path:
    """Write a WikiNote to wiki/{para}/{id}.md with YAML frontmatter."""
    ensure_directories()
    valid_para = note.para if note.para in PARA_CATEGORIES else "Resources"
    target_dir = WIKI_DIR / valid_para
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / f"{note.id}.md"
    frontmatter = {
        "id": note.id,
        "raw_id": note.raw_id,
        "para": valid_para,
        "tags": sorted(set(note.tags)),
        "summary": note.summary,
        "created": note.created,
        "links": sorted(set(note.links)),
    }
    content = f"---\n{yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)}---\n\n{note.body.rstrip()}\n"
    _atomic_write(file_path, content)
    return file_path


def read_wiki_notes() -> List[WikiNote]:
    """Parse all Markdown wiki pages with valid YAML frontmatter."""
    ensure_directories()
    notes: List[WikiNote] = []
    for filepath in sorted(WIKI_DIR.glob("**/*.md")):
        try:
            with open(filepath, "r", encoding="utf-8") as handle:
                raw_text = handle.read()
            if not (raw_text.startswith("---\n") or raw_text.startswith("---\r\n")):
                continue
            closing = raw_text.find("\n---", 4)
            if closing == -1:
                raise ValueError("missing frontmatter terminator")
            fm_data = yaml.safe_load(raw_text[4:closing]) or {}
            if not isinstance(fm_data, dict):
                raise ValueError("frontmatter must be a mapping")
            notes.append(WikiNote(
                id=str(fm_data.get("id", filepath.stem)),
                raw_id=str(fm_data.get("raw_id", "")),
                para=str(fm_data.get("para", filepath.parent.name)),
                tags=[str(tag) for tag in (fm_data.get("tags", []) or [])],
                summary=str(fm_data.get("summary", "")),
                created=str(fm_data.get("created", "")),
                links=[str(link) for link in (fm_data.get("links", []) or [])],
                body=raw_text[closing + 4:].strip(),
            ))
        except (OSError, TypeError, ValueError, yaml.YAMLError) as exc:
            print(f"Warning: Failed to parse wiki note at {filepath}: {exc}")
    return notes
