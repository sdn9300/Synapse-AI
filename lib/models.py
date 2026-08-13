"""
Data models and dataclass definitions for SecondSelf.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class CaptureMeta:
    """Metadata recorded for every raw capture in raw/{id}/meta.json."""
    id: str                      # Format: YYYY-MM-DD_{uuid8}
    timestamp: str               # ISO 8601 string
    type: str                    # "note" | "link" | "file"
    source: str                  # Original URL, filepath, or "stdin"
    original_filename: Optional[str] = None
    content_hash: str = ""       # SHA-256 string for deduplication


@dataclass
class CaptureResult:
    """Return type from capture functions."""
    id: str
    path: str
    type: str


@dataclass
class WikiNote:
    """Structured Wiki page representation."""
    id: str                      # Unique short ID
    raw_id: str                  # Corresponding raw capture folder ID
    para: str                    # "Projects" | "Areas" | "Resources" | "Archives"
    tags: List[str]              # List of keywords
    summary: str                 # One-line executive summary
    created: str                 # ISO timestamp
    links: List[str] = field(default_factory=list)  # List of target note IDs
    body: str = ""               # Markdown body text


@dataclass
class GraphNode:
    """Node in vis-network graph payload."""
    id: str
    label: str                   # Display title/summary
    para: str                    # PARA group
    tags: List[str]
    summary: str
    content_preview: str         # First 200 chars
    group: str                   # Used for vis-network node coloring


@dataclass
class GraphEdge:
    """Edge connecting related notes in vis-network graph payload."""
    source: str
    target: str
    weight: float                # Cosine similarity score
    type: str = "related"


@dataclass
class AskResult:
    """Result returned by RAG Q&A query engine."""
    answer: str
    sources: List[Dict[str, Any]] # List of [{id, summary, relevance_score, para}]
