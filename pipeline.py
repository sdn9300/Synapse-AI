"""Master orchestrator for classification, linking, and graph generation."""

import argparse

from build_graph import process_build_graph
from classify import process_classification
from link import process_auto_linking


def run_pipeline(mode: str = "process") -> dict:
    """Run one pipeline stage or the complete processing flow."""
    if mode not in {"classify", "link", "graph", "process"}:
        raise ValueError("mode must be classify, link, graph, or process")

    result = {"mode": mode, "classified": 0, "links_added": 0, "graph_nodes": 0, "graph_edges": 0}
    print(f"=== Starting SecondSelf Pipeline (mode: {mode}) ===")

    if mode in {"classify", "process"}:
        result["classified"] = process_classification()
    if mode in {"link", "process"}:
        result["links_added"] = process_auto_linking()
    if mode in {"graph", "process"}:
        graph = process_build_graph()
        result["graph_nodes"] = graph["metadata"]["node_count"]
        result["graph_edges"] = graph["metadata"]["edge_count"]

    print("=== Pipeline execution completed ===")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="SecondSelf pipeline orchestrator")
    parser.add_argument("mode", nargs="?", default="process", choices=["classify", "link", "graph", "process"])
    args = parser.parse_args()
    run_pipeline(args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
