# SecondSelf architecture

## System shape

SecondSelf is a local filesystem application with a staged maintenance pipeline:

    capture -> raw storage -> extraction/classification -> wiki Markdown
             -> content-aware embeddings -> generated links -> graph export
             -> vector retrieval -> grounded answer synthesis

The raw vault is the source record. The wiki vault is a generated, searchable representation. The graph and embedding cache are derived state and can be rebuilt.

## Components

### Capture

capture.py accepts text notes, public HTTP(S) links, and local files. It validates inputs, computes a SHA-256 content hash, and reuses an existing capture when content is identical.

### Storage

lib/storage.py owns the project paths and serialization rules. JSON, Markdown, and raw files are written through temporary files followed by replacement. Individual corrupt raw records are reported and skipped so one damaged item does not hide the rest of the vault.

### Extraction and classification

classify.py handles plain text, the first ten pages of PDFs, and public web pages. URL fetching rejects obvious local/private destinations, does not follow redirects, and uses a short timeout. PARA classification uses the Groq API when GROQ_API_KEY is configured and falls back to deterministic heuristics.

A capture is marked processed only after its wiki page is successfully written. Failed captures remain retryable on the next run.

### Embeddings and linking

lib/embeddings.py uses all-MiniLM-L6-v2 when available. If the dependency/model cannot load, it uses a stable 384-dimensional hashed bag-of-words fallback. Cached vectors include the model, dimension, and content fingerprints.

link.py compares each note pair once, adds symmetric generated relationships at the configured threshold, removes stale generated Related Note lines, and preserves user links where possible.

### Graph export

build_graph.py converts wiki notes into nodes and undirected edges. It ignores wikilinks in fenced and inline Markdown code examples, collapses reciprocal references into one edge, keeps the strongest evidence weight, and writes deterministic ordering to data/graph.json.

static/graph.html can fetch graph.json when served directly. The Streamlit app embeds the current graph payload so it does not depend on a filesystem URL inside an iframe.

### Retrieval and synthesis

ask.py embeds the question, ranks available note vectors, rejects the query when the best score is below 0.15, and passes only the top context to lib/llm.py. The generation prompt requires answers to stay within the supplied notes and cite note IDs. Without a working API key, a local summary fallback is returned.

### User interface and integrations

app.py provides capture forms, the ask interface, metrics, graph exploration, and a pipeline button. mcp_server.py exposes Python functions plus a simple JSON-lines adapter for external callers; it is not a standards-compliant MCP SDK server.

## Derived state

- data/index.json: raw processing registry and graph timestamp.
- data/embeddings.pkl: versioned vectors and content fingerprints.
- data/graph.json: graph nodes, unique edges, and metadata.
- wiki/synthesis/health_report.md: lint output.
- wiki/synthesis/YYYY-Www.md: weekly digest output.
- wiki/log.md: scheduler maintenance log.

All derived state can be regenerated from raw/ and wiki/ by running:

    python pipeline.py process
    python lint.py

## Current boundaries

The repository is a robust local prototype, not a hosted multi-user service. It does not currently implement authentication, a database/vector service, RAGAS evaluation, tracing, background workers, or cloud deployment manifests. The evaluation script provides smoke metrics and regression checks; it is not a substitute for a human-reviewed retrieval benchmark.
