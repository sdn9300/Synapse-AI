"""Multi-source capture CLI and library functions for SecondSelf."""

import argparse
from datetime import datetime, timezone
from pathlib import Path

from lib.models import CaptureMeta, CaptureResult
from lib.storage import (
    RAW_DIR,
    content_hash,
    find_duplicate_capture,
    generate_capture_id,
    write_raw_capture,
)


def _duplicate_result(meta: CaptureMeta, capture_type: str) -> CaptureResult:
    print(f"Duplicate content detected; reusing raw/{meta.id}.")
    return CaptureResult(id=meta.id, path=str(RAW_DIR / meta.id), type=capture_type)


def capture_note(text: str) -> CaptureResult:
    text = (text or "").strip()
    if not text:
        raise ValueError("Note text cannot be empty.")
    duplicate = find_duplicate_capture(text)
    if duplicate:
        return _duplicate_result(duplicate, "note")

    capture_id = generate_capture_id()
    meta = CaptureMeta(
        id=capture_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        type="note",
        source="stdin",
        content_hash=content_hash(text),
    )
    folder = write_raw_capture(meta, text)
    print(f"Captured note -> raw/{capture_id}")
    return CaptureResult(id=capture_id, path=str(folder), type="note")


def capture_link(url: str, notes: str = "") -> CaptureResult:
    url = (url or "").strip()
    if not url:
        raise ValueError("URL cannot be empty.")
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("URL must start with http:// or https://")

    content_body = f"URL: {url}\nNotes: {notes}\n" if notes else f"URL: {url}\n"
    duplicate = find_duplicate_capture(content_body)
    if duplicate:
        return _duplicate_result(duplicate, "link")

    capture_id = generate_capture_id()
    meta = CaptureMeta(
        id=capture_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        type="link",
        source=url,
        content_hash=content_hash(content_body),
    )
    folder = write_raw_capture(meta, content_body)
    print(f"Captured link -> raw/{capture_id}")
    return CaptureResult(id=capture_id, path=str(folder), type="link")


def capture_file(filepath: str) -> CaptureResult:
    path_obj = Path((filepath or "").strip())
    if not path_obj.exists():
        raise FileNotFoundError(f"File does not exist: {filepath}")
    if not path_obj.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    file_bytes = path_obj.read_bytes()
    if not file_bytes:
        raise ValueError(f"File is empty: {filepath}")
    duplicate = find_duplicate_capture(file_bytes)
    if duplicate:
        return _duplicate_result(duplicate, "file")

    capture_id = generate_capture_id()
    meta = CaptureMeta(
        id=capture_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        type="file",
        source=str(path_obj.resolve()),
        original_filename=path_obj.name,
        content_hash=content_hash(file_bytes),
    )
    folder = write_raw_capture(meta, file_bytes)
    print(f"Captured file '{path_obj.name}' -> raw/{capture_id}")
    return CaptureResult(id=capture_id, path=str(folder), type="file")


def main() -> int:
    parser = argparse.ArgumentParser(description="SecondSelf multi-source capture CLI")
    subparsers = parser.add_subparsers(dest="command")

    note_parser = subparsers.add_parser("note", help="Capture a text note")
    note_parser.add_argument("text")

    link_parser = subparsers.add_parser("link", help="Capture a web URL")
    link_parser.add_argument("url")
    link_parser.add_argument("--notes", default="")

    file_parser = subparsers.add_parser("file", help="Capture a local file")
    file_parser.add_argument("filepath")

    args = parser.parse_args()
    try:
        if args.command == "note":
            capture_note(args.text)
        elif args.command == "link":
            capture_link(args.url, notes=args.notes)
        elif args.command == "file":
            capture_file(args.filepath)
        else:
            print("Use one of: python capture.py note, link, or file.")
            return 2
    except (FileNotFoundError, ValueError, OSError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
