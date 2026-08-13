# SecondSelf - Personal AI Second Brain

SecondSelf is a local-first personal knowledge system. It captures notes, links, and documents, organizes them into a PARA-style Markdown wiki, creates local vector links, exposes a knowledge graph, and answers questions using retrieval over the curated wiki.

## What is implemented

- Multi-source capture through the CLI and Streamlit UI.
- Immutable raw records under raw/ with timestamps and SHA-256 content hashes.
- Classification into Projects, Areas, Resources, and Archives using Groq when configured, with a local heuristic fallback.
- Local all-MiniLM-L6-v2 embeddings with a stable hashed fallback when the model cannot load.
- Content-aware embedding cache refresh and symmetric similarity links.
- Deterministic graph export to data/graph.json.
- RAG search with a minimum relevance guardrail and cited source metadata.
- Vault linting for broken links, orphan pages, and near-duplicates.
- Weekly digest generation and a JSON-lines adapter in mcp_server.py for external callers.

This is a local prototype. It does not currently provide a standards-compliant MCP SDK server, Qdrant-backed retrieval, RAGAS scoring, authentication, or cloud deployment configuration.

## Quickstart

Create and activate a virtual environment:

    python -m venv .venv
    .venv\Scripts\activate          # Windows
    source .venv/bin/activate         # macOS/Linux

Install dependencies:

    python -m pip install -r requirements.txt

Optionally configure Groq:

    Copy-Item .env.example .env      # PowerShell
    # Edit .env and set GROQ_API_KEY

Run the complete maintenance pipeline:

    python pipeline.py process

Capture content:

    python capture.py note "A note about a project"
    python capture.py link "https://example.com" --notes "Why it matters"
    python capture.py file .\ARCHITECTURE.md

Query the vault:

    python ask.py "What are the core goals of SecondSelf?"

Run health checks:

    python lint.py
    python eval_benchmark.py
    python -m unittest -v

Launch the UI:

    streamlit run app.py

## Repository layout

    raw/                 Immutable captured source records
    wiki/                Curated Markdown wiki, grouped by PARA category
    data/index.json      Processing registry and graph timestamp
    data/graph.json      Graph nodes, unique edges, and metadata
    data/embeddings.pkl  Local embedding cache (ignored by Git)
    static/graph.html    Standalone graph viewer
    lib/                 Shared models, storage, Markdown, and embedding helpers
    capture.py           Capture CLI and library functions
    classify.py          Extraction and PARA classification
    link.py              Similarity-based link rebuilding
    build_graph.py       Graph JSON export
    ask.py               Retrieval and grounded answer synthesis
    app.py               Streamlit interface
    lint.py              Vault health report
    digest.py             Weekly digest generation
    scheduler.py         Maintenance run and audit log
    mcp_server.py        JSON-lines integration adapter
    test_secondself.py   unittest suite

## Pipeline behavior

1. Capture writes a raw record. Duplicate content reuses the existing raw capture.
2. Classification extracts text and writes a wiki page. A failed item remains retryable.
3. Linking refreshes vectors whose note content changed and rebuilds generated related-note links.
4. Graph export deduplicates relationships and writes deterministic node/edge ordering.
5. Ask embeds the question, applies the 0.15 minimum similarity threshold, and synthesizes only retrieved context.

Raw records are never edited by the processing pipeline. Generated wiki pages, graph state, embedding state, digest reports, and health reports are maintained artifacts.

## Configuration

Supported environment variable:

    GROQ_API_KEY=your_groq_api_key_here

When the key is absent or the request fails, classification and answer synthesis use local fallback behavior. Link fetching is restricted to public HTTP(S) hosts and uses a short timeout.

## Notes for contributors

- Keep generated embedding state out of source control.
- Run unittest, lint, and the pipeline before committing changes.
- Treat raw/ as source data; do not hand-edit captured records.
- Keep documentation claims aligned with installed dependencies and actual runtime behavior.
