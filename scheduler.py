"""Run maintenance and append an auditable vault summary."""

import json
from datetime import datetime, timezone

from pipeline import run_pipeline
from lib.storage import GRAPH_FILE, WIKI_DIR, read_raw_captures, read_wiki_notes


LOG_FILE = WIKI_DIR / "log.md"


def record_maintenance_log() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] Triggering SecondSelf maintenance run.")
    result = run_pipeline("process")

    graph_nodes = result["graph_nodes"]
    graph_edges = result["graph_edges"]
    entry = (
        f"\n### Maintenance Run - {timestamp}\n"
        f"- **Raw Captures:** {len(read_raw_captures())}\n"
        f"- **Wiki Pages:** {len(read_wiki_notes())}\n"
        f"- **Graph:** {graph_nodes} nodes | {graph_edges} unique edges\n"
        f"- **Processed Captures:** {result['classified']}\n"
        f"- **New Links:** {result['links_added']}\n"
        f"- **Status:** Completed\n"
    )
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.write_text("# SecondSelf Maintenance and Audit Log\n", encoding="utf-8")
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(entry)
    print("Logged maintenance entry -> wiki/log.md")
    return entry


if __name__ == "__main__":
    record_maintenance_log()
