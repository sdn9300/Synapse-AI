"""Markdown helpers shared by graph and vault-health tooling."""

import re
from typing import Set


_FENCED_BLOCK_RE = re.compile(r"\x60\x60\x60.*?\x60\x60\x60", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"\x60[^\x60\n]+\x60")
_WIKILINK_RE = re.compile(r"\[\[([A-Za-z0-9_-]+)\]\]")


def extract_wikilinks(markdown: str) -> Set[str]:
    """Return wikilink targets from prose, ignoring Markdown code examples."""
    without_fences = _FENCED_BLOCK_RE.sub("", markdown or "")
    without_code = _INLINE_CODE_RE.sub("", without_fences)
    return set(_WIKILINK_RE.findall(without_code))


def extract_related_links(markdown: str) -> Set[str]:
    """Return links written by the auto-linker as Related Note lines."""
    pattern = re.compile(r"^\s*Related Note:\s*\[\[([A-Za-z0-9_-]+)\]\]\s*$", re.MULTILINE)
    return set(pattern.findall(markdown or ""))


def remove_related_link_lines(markdown: str) -> str:
    """Remove auto-generated related-note lines without touching user prose."""
    pattern = re.compile(r"\n?[ \t]*Related Note:\s*\[\[[A-Za-z0-9_-]+\]\][ \t]*(?=\n|$)", re.MULTILINE)
    return pattern.sub("", markdown or "").rstrip()
