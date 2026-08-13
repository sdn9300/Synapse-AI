"""Export the wiki vault as a deterministic vis-network graph payload."""

import json
from datetime import datetime, timezone
from typing import Any, Dict, Tuple

from lib.markdown import extract_wikilinks
from lib.storage import DATA_DIR, GRAPH_FILE, load_index, read_wiki_notes, save_index


GROUP_COLORS = {
    "Projects": "#4CAF50",
    "Areas": "#2196F3",
    "Resources": "#FF9800",
    "Archives": "#9E9E9E",
}


def process_build_graph() -> Dict[str, Any]:
    notes = read_wiki_notes()
    note_ids = {note.id for note in notes}
    nodes = []
    edge_weights: Dict[Tuple[str, str], float] = {}

    for note in notes:
        preview = note.body[:200].replace("\n", " ").strip()
        if len(note.body) > 200:
            preview += "..."
        nodes.append({
            "id": note.id,
            "label": (note.summary[:60] if note.summary else note.id),
            "para": note.para,
            "tags": note.tags,
            "summary": note.summary,
            "content_preview": preview,
            "group": note.para,
            "color": GROUP_COLORS.get(note.para, "#9C27B0"),
        })

        targets = set(note.links) | extract_wikilinks(note.body)
        for target in targets:
            if target not in note_ids or target == note.id:
                continue
            key = tuple(sorted((note.id, target)))
            # An explicit frontmatter link is stronger evidence than prose.
            candidate_weight = 0.8 if target in note.links else 0.75
            edge_weights[key] = max(edge_weights.get(key, 0.0), candidate_weight)

    edges = [
        {"source": source, "target": target, "weight": weight, "type": "related"}
        for (source, target), weight in sorted(edge_weights.items())
    ]
    generated_at = datetime.now(timezone.utc).isoformat()
    payload = {
        "nodes": sorted(nodes, key=lambda node: node["id"]),
        "edges": edges,
        "metadata": {
            "generated_at": generated_at,
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = GRAPH_FILE.with_name(f".{GRAPH_FILE.name}.tmp")
    with open(temp_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
        handle.flush()
    temp_path.replace(GRAPH_FILE)

    index = load_index()
    index["last_graph_build"] = generated_at
    save_index(index)
    print(f"Graph exported -> data/graph.json ({len(nodes)} nodes, {len(edges)} unique edges)")
    return payload


if __name__ == "__main__":
    process_build_graph()
