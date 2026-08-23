"""Import Markdown notes dropped into the Obsidian Inbox.

The Inbox is a user-facing capture surface.  Notes are copied into immutable
raw storage by the normal capture layer, then moved to Inbox/Processed so the
same note is not imported on every pipeline run.
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from capture import capture_file
from lib.markdown import extract_frontmatter
from lib.storage import PROJECT_ROOT, WIKI_DIR, content_hash, load_index, save_index


INBOX_DIR = WIKI_DIR / "Inbox"
PROCESSED_DIR = INBOX_DIR / "Processed"
VALID_PARA = {"Projects", "Areas", "Resources", "Archives"}


def ensure_inbox() -> None:
    """Create the Inbox structure and starter template when needed."""

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    template = INBOX_DIR / "_template.md"
    if not template.exists():
        template.write_text(
            "---\n"
            "title: \n"
            "para: \n"
            "tags: []\n"
            "summary: \n"
            "---\n\n"
            "Write your note here...\n",
            encoding="utf-8",
        )


def _classification_override(frontmatter: Dict[str, Any]) -> Dict[str, Any]:
    """Extract optional, safe classification hints from note frontmatter."""

    override: Dict[str, Any] = {}
    para = frontmatter.get("para")
    if isinstance(para, str) and para.strip() in VALID_PARA:
        override["para"] = para.strip()

    tags = frontmatter.get("tags")
    if isinstance(tags, str):
        tags = [item.strip() for item in tags.split(",") if item.strip()]
    if isinstance(tags, list):
        clean_tags = [item.strip() for item in tags if isinstance(item, str) and item.strip()]
        if clean_tags:
            override["tags"] = clean_tags

    summary = frontmatter.get("summary")
    if isinstance(summary, str) and summary.strip():
        override["summary"] = summary.strip()
    return override


def ingest_obsidian_inbox() -> int:
    """Capture pending Inbox notes and move them to the processed area.

    Only direct Markdown children of ``wiki/Inbox`` are considered.  The
    underscore-prefixed template is intentionally ignored, and files already
    in ``Processed`` are never scanned.
    """

    ensure_inbox()
    index = load_index()
    registry = index.setdefault("obsidian_inbox", {})
    overrides = index.setdefault("classification_overrides", {})
    imported = 0

    for note_path in sorted(INBOX_DIR.glob("*.md")):
        if note_path.name.startswith("_"):
            continue
        content = note_path.read_bytes()
        if not content.strip():
            continue
        digest = content_hash(content)
        registry_key = note_path.relative_to(PROJECT_ROOT).as_posix()
        result = capture_file(str(note_path))
        decoded = content.decode("utf-8", errors="replace")
        frontmatter, _ = extract_frontmatter(decoded)
        override = _classification_override(frontmatter)
        if override:
            overrides[result.id] = override

        destination = PROCESSED_DIR / f"{note_path.stem}__{result.id}{note_path.suffix}"
        shutil.move(str(note_path), str(destination))
        registry[registry_key] = {
            "content_hash": digest,
            "raw_id": result.id,
            "status": "captured",
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "processed_path": destination.relative_to(PROJECT_ROOT).as_posix(),
        }
        imported += 1

    save_index(index)
    return imported


if __name__ == "__main__":
    print(f"Imported {ingest_obsidian_inbox()} Obsidian Inbox note(s).")
