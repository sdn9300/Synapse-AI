# SecondSelf evaluation plan

This document describes the checks that are actually available in the repository. It distinguishes deterministic local health checks from future LLM-as-a-judge evaluation.

## Automated checks

Run:

    python -m unittest -v
    python lint.py
    python eval_benchmark.py

The unit suite covers capture ID and hash behavior, stable fallback embeddings, cosine similarity, input validation, fenced-code wikilink parsing, graph edge uniqueness, RAG contracts, and the JSON-lines integration API.

The lint command reports:

- Broken wikilinks in frontmatter or prose.
- Orphan pages with no incoming or outgoing references.
- Near-duplicate note pairs with cosine similarity at least 0.92.
- A Markdown report at wiki/synthesis/health_report.md.

The benchmark reports:

- Wiki page count.
- Graph node and unique-edge counts.
- Link density, calculated as 2E/V.
- Lint totals.
- Query-to-answer embedding similarity for three smoke-test questions.
- Retrieved source IDs.

## Current acceptance criteria

- Python files compile successfully.
- The complete pipeline runs without silently swallowing stage import failures.
- Re-running the pipeline does not create duplicate graph edges or duplicate generated related-note lines.
- Embeddings are refreshed when note content changes.
- A query with no meaningful match returns the no-notes response and no fabricated source list.
- Raw capture files remain unchanged after processing.
- Corrupt individual raw records do not prevent valid records from being read.

## Interpretation

The local benchmark is a smoke and regression suite, not a complete measure of answer quality. Query-to-answer cosine similarity is only a proxy for relevance. The project does not currently install or execute RAGAS, Qdrant, tracing, or a human-reviewed ground-truth dataset. Those should be added before claiming production-grade retrieval quality.

Suggested future evaluation:

1. Create a small, manually verified question/context dataset.
2. Measure hit rate and context precision at K=3 and K=5.
3. Add answer faithfulness review against retrieved note bodies.
4. Track capture, classification, linking, and UI latency separately.
5. Run the suite in CI against a temporary fixture vault rather than the user's live data.
