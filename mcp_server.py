"""
Model Context Protocol (MCP) Server for SecondSelf (Phase 5 / Module M6).
Exposes the Personal AI Second Brain as a callable MCP tool server for external agent orchestrators.
"""

import sys
import json
import argparse
from typing import Dict, Any

from ask import ask
from lib.storage import read_wiki_notes, load_index
from capture import capture_note, capture_link, capture_file
from pipeline import run_pipeline


def search_second_brain(query: str, top_k: int = 5) -> Dict[str, Any]:
    """MCP Tool: Search natural language query over SecondSelf knowledge vault."""
    res = ask(query, top_k=top_k)
    return {
        "answer": res.answer,
        "sources": res.sources,
    }


def get_wiki_page(note_id: str) -> Dict[str, Any]:
    """MCP Tool: Retrieve specific wiki page by note ID."""
    notes = read_wiki_notes()
    for note in notes:
        if note.id == note_id:
            return {
                "id": note.id,
                "raw_id": note.raw_id,
                "para": note.para,
                "tags": note.tags,
                "summary": note.summary,
                "created": note.created,
                "links": note.links,
                "body": note.body,
            }
    return {"error": f"Note ID '{note_id}' not found in wiki vault."}


def ingest_raw_content(content_type: str, content: str, source_info: str = "mcp") -> Dict[str, Any]:
    """MCP Tool: Ingest text note, URL link, or local file into SecondSelf raw store and trigger pipeline."""
    content_type = content_type.lower().strip()
    if content_type == "note":
        res = capture_note(content)
    elif content_type == "link":
        res = capture_link(content, notes=source_info)
    elif content_type == "file":
        res = capture_file(content)
    else:
        return {"error": f"Unsupported content_type '{content_type}'. Must be 'note', 'link', or 'file'."}

    # Trigger processing pipeline
    run_pipeline("process")

    return {
        "status": "success",
        "capture_id": res.id,
        "path": res.path,
        "type": res.type,
    }


def process_mcp_request(request_json: str) -> str:
    """Process JSON RPC request from standard input."""
    try:
        data = json.loads(request_json)
        tool_name = data.get("tool")
        args = data.get("args", {})

        if tool_name == "search_second_brain":
            result = search_second_brain(args.get("query", ""), top_k=args.get("top_k", 5))
        elif tool_name == "get_wiki_page":
            result = get_wiki_page(args.get("note_id", ""))
        elif tool_name == "ingest_raw_content":
            result = ingest_raw_content(
                args.get("content_type", "note"),
                args.get("content", ""),
                source_info=args.get("source_info", "mcp"),
            )
        else:
            result = {"error": f"Unknown tool name '{tool_name}'."}

        return json.dumps({"status": "ok", "result": result})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def main():
    parser = argparse.ArgumentParser(description="SecondSelf MCP Tool Server")
    parser.add_argument("--tool", type=str, help="Tool to invoke: search_second_brain | get_wiki_page | ingest_raw_content")
    parser.add_argument("--query", type=str, help="Query string for search_second_brain")
    parser.add_argument("--note_id", type=str, help="Note ID for get_wiki_page")

    args = parser.parse_args()

    if args.tool == "search_second_brain":
        res = search_second_brain(args.query or "What is SecondSelf?")
        print(json.dumps(res, indent=2))
    elif args.tool == "get_wiki_page":
        res = get_wiki_page(args.note_id or "")
        print(json.dumps(res, indent=2))
    else:
        # Standard stdin JSON RPC mode
        print("SecondSelf JSON-lines adapter listening on stdin...", file=sys.stderr)
        for line in sys.stdin:
            if line.strip():
                response = process_mcp_request(line.strip())
                print(response)
                sys.stdout.flush()


if __name__ == "__main__":
    main()
