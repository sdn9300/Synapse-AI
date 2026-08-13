# SecondSelf implementation status

## Completed

- Phase 0: filesystem layout, dataclasses, hashing, and state files.
- Phase 1: CLI capture for notes, links, and local files.
- Phase 2: extraction, PARA classification, local embeddings, and similarity linking.
- Phase 3: graph export and standalone vis-network viewer.
- Phase 4: RAG search and Streamlit interface.
- Phase 5: vault linting, weekly digest generation, maintenance logging, and JSON-lines integration adapter.
- Quality pass: atomic writes, duplicate reuse, retryable classification failures, deterministic fallback vectors, cache invalidation, graph edge deduplication, link parser filtering, and automated tests.

## Verification commands

    python -m compileall -q .
    python -m unittest -v
    python pipeline.py process
    python lint.py
    python eval_benchmark.py

## Current measured state

The sample vault currently contains 14 wiki pages, 2 unique graph edges, zero broken wikilinks, 10 orphan pages, and one near-duplicate pair. The orphan count is a property of the current sample content and should be reduced by capturing related notes or adding intentional links; it should not be hidden by synthetic graph edges.

## Deliberate non-goals

The current implementation does not claim a standards-compliant MCP server, Qdrant retrieval, RAGAS evaluation, tracing, authentication, or cloud deployment. Those are separate follow-up initiatives and should only be advertised after their dependencies, tests, and operational configuration are added.

## Next improvements

1. Add fixture-based tests that run against temporary raw and wiki directories rather than the live vault.
2. Add content-level deduplication review for near-duplicate wiki pages.
3. Add a reviewed question/context dataset for retrieval precision and faithfulness.
4. Add a proper MCP SDK server only if external orchestration requires it.
5. Add background scheduling and deployment configuration only after the local workflow is stable.
