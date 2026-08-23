"""Extract raw captures, classify them, and write structured wiki pages."""

import ipaddress
import re
import socket
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import pypdf
import requests
from bs4 import BeautifulSoup

from lib.llm import classify_content
from lib.markdown import strip_frontmatter
from lib.models import WikiNote
from lib.storage import load_index, read_raw_captures, save_index, write_wiki_note


def _is_safe_public_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    hostname = parsed.hostname.lower()
    if hostname in {"localhost", "localhost.localdomain"} or hostname.endswith(".local"):
        return False
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(hostname, None)}
    except socket.gaierror:
        return False
    for address in addresses:
        ip = ipaddress.ip_address(address)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return False
    return True


def _fetch_page_text(url: str) -> str:
    if not _is_safe_public_url(url):
        return ""
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "SecondSelf/1.0"},
            allow_redirects=False,
        )
        if response.status_code not in {200, 203}:
            return ""
        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup(["script", "style", "nav", "header", "footer", "form"]):
            element.decompose()
        return soup.get_text(separator=" ", strip=True)[:5000]
    except requests.RequestException as exc:
        print(f"Notice: Could not fetch URL '{url}': {exc}")
        return ""


def extract_text_from_raw(meta, content, cfile_path: Path) -> str:
    """Extract clean text from a note, link, PDF, or text-like file."""
    if meta.type == "note":
        text = content if isinstance(content, str) else content.decode("utf-8", errors="ignore")
        return strip_frontmatter(text)

    if meta.type == "link":
        text = content if isinstance(content, str) else content.decode("utf-8", errors="ignore")
        url_match = re.search(r"URL:\s*(https?://[^\s]+)", text)
        url = url_match.group(1) if url_match else meta.source
        page_text = _fetch_page_text(url)
        return f"{text}\n\nWeb Page Content:\n{page_text}" if page_text else text

    if meta.type == "file":
        if cfile_path.suffix.lower() == ".pdf":
            try:
                reader = pypdf.PdfReader(cfile_path)
                pages = [page.extract_text() or "" for page in reader.pages[:10]]
                extracted = "\n".join(pages).strip()
                if extracted:
                    return extracted
            except Exception as exc:
                print(f"Warning: PDF extraction failed for '{cfile_path.name}': {exc}")
            return f"Filename: {meta.original_filename or cfile_path.name}"
        if isinstance(content, str):
            return strip_frontmatter(content) if cfile_path.suffix.lower() in {".md", ".markdown"} else content
        try:
            decoded = content.decode("utf-8")
            return strip_frontmatter(decoded) if cfile_path.suffix.lower() in {".md", ".markdown"} else decoded
        except UnicodeDecodeError:
            return f"Binary file: {meta.original_filename or cfile_path.name}"

    return str(content)


def process_classification() -> int:
    """Process each unprocessed capture; leave failed items retryable."""
    index = load_index()
    raw_processed = index.setdefault("raw_processed", {})
    processed_count = 0

    for meta, content, content_path in read_raw_captures():
        if meta.id in raw_processed:
            continue
        print(f"Classifying raw capture '{meta.id}' ({meta.type})...")
        try:
            extracted = extract_text_from_raw(meta, content, content_path).strip()
            if not extracted:
                raise ValueError("extracted content is empty")
            classified = classify_content(extracted, source_type=meta.type)
            override = index.get("classification_overrides", {}).get(meta.id, {})
            if isinstance(override, dict):
                if override.get("para") in {"Projects", "Areas", "Resources", "Archives"}:
                    classified["para"] = override["para"]
                if isinstance(override.get("tags"), list) and override["tags"]:
                    classified["tags"] = [str(tag) for tag in override["tags"]]
                if isinstance(override.get("summary"), str) and override["summary"].strip():
                    classified["summary"] = override["summary"].strip()
            note_id = meta.id.rsplit("_", 1)[-1]
            note = WikiNote(
                id=note_id,
                raw_id=meta.id,
                para=classified["para"],
                tags=classified["tags"],
                summary=classified["summary"],
                created=meta.timestamp or datetime.now(timezone.utc).isoformat(),
                body=extracted,
            )
            wiki_path = write_wiki_note(note)
            raw_processed[meta.id] = {
                "status": "processed",
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "wiki_path": str(wiki_path),
                "para": note.para,
                "note_id": note.id,
            }
            processed_count += 1
            print(f"  -> Generated wiki/{note.para}/{note.id}.md")
        except Exception as exc:
            print(f"Warning: Failed to classify '{meta.id}'; will retry: {exc}")

    index["raw_processed"] = raw_processed
    save_index(index)
    print(f"Classification complete. Processed {processed_count} new captures.")
    return processed_count


if __name__ == "__main__":
    process_classification()
