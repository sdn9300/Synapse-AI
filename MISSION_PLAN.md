# SecondSelf mission and maintenance plan

## Mission

Build a private, local-first knowledge workflow that makes captured material searchable and connected without treating generated answers as a replacement for source notes.

## Operating loop

1. Capture source material into raw/.
2. Process unindexed captures into PARA wiki pages.
3. Refresh embeddings when note content changes.
4. Rebuild generated links and graph state.
5. Ask questions with a relevance threshold and source metadata.
6. Run lint and evaluation checks.
7. Generate a weekly digest and maintenance log when desired.

## Reliability principles

- Raw captures are source records and are not edited by agents.
- Derived files must be rebuildable.
- Failed records remain retryable.
- Generated links must be distinguishable from user prose.
- Metrics should describe the current vault, not aspirational infrastructure.
- External network access is bounded and optional.

## Current status

The local capture, classification, linking, graph, RAG, UI, lint, digest, scheduler, and JSON-lines adapter workflows are implemented. The current sample vault is healthy with zero broken wikilinks, but it has 10 orphan pages and one near-duplicate pair. That is a content-quality follow-up, not a reason to invent relationships.

## Deferred work

- Temporary-fixture integration tests and CI.
- Human-reviewed retrieval benchmark.
- Proper MCP SDK transport, if required by consumers.
- Optional vector database backend for larger vaults.
- Authentication, background workers, tracing, and deployment manifests.
