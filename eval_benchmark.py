"""Report measurable vault and retrieval health metrics."""

import json
from typing import Any, Dict

from ask import ask
from build_graph import process_build_graph
from lib.embeddings import cosine_similarity, embed_text
from lib.storage import GRAPH_FILE, read_wiki_notes
from lint import run_vault_lint


def run_evaluation_suite() -> Dict[str, Any]:
    notes = read_wiki_notes()
    lint = run_vault_lint()
    graph = process_build_graph()
    node_count = graph["metadata"]["node_count"]
    edge_count = graph["metadata"]["edge_count"]
    queries = [
        "What are the core goals of SecondSelf?",
        "Explain the DevOps Phase 14 capstone requirements",
        "What local embedding model is used for auto-linking?",
    ]
    retrieval = []
    for query in queries:
        result = ask(query, top_k=3)
        relevance = cosine_similarity(embed_text(query), embed_text(result.answer))
        retrieval.append({
            "query": query,
            "answer_relevance": round(relevance, 3),
            "sources": [source["id"] for source in result.sources],
        })

    report = {
        "notes": len(notes),
        "graph_nodes": node_count,
        "graph_edges": edge_count,
        "link_density": round((2 * edge_count) / max(1, node_count), 3),
        "broken_links": len(lint["broken_links"]),
        "orphan_pages": len(lint["orphans"]),
        "near_duplicate_pairs": len(lint["near_duplicates"]),
        "retrieval": retrieval,
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    run_evaluation_suite()
