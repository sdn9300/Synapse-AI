# SecondSelf data conventions

## Storage

- raw/{capture-id}/ is the immutable source record.
- raw/{capture-id}/meta.json stores id, timestamp, type, source, original filename, and SHA-256 content_hash.
- wiki/{Projects,Areas,Resources,Archives}/ contains generated Markdown pages.
- data/index.json stores processed raw IDs and the last graph build timestamp.
- data/embeddings.pkl stores versioned vectors, content fingerprints, model name, and vector dimension.
- data/graph.json stores graph nodes, unique undirected edges, and generation metadata.

## Wiki frontmatter

Every generated wiki page uses:

    ---
    id: a1b2c3d4
    raw_id: 2026-08-02_a1b2c3d4
    para: Projects
    tags:
      - ai
      - architecture
    summary: One-line executive summary.
    created: 2026-08-02T20:10:00+00:00
    links:
      - e5f6g7h8
    ---

The para value must be Projects, Areas, Resources, or Archives. Links contain note IDs, not file paths.

## Processing rules

1. Capture computes a SHA-256 digest and reuses an existing raw record with the same content.
2. Classification only marks a raw ID processed after its wiki page is written successfully.
3. The auto-linker stores generated links as Related Note lines and rebuilds those links from the current threshold. User prose and frontmatter links are preserved when possible.
4. Graph construction ignores wikilinks inside fenced code blocks and collapses reciprocal or duplicate references into one edge.
5. RAG retrieval uses the note-plus-body embedding and rejects the result when the best cosine score is below 0.15.
6. Lint reports broken references, pages with no incoming or outgoing links, and vector near-duplicates.

## Safety and recovery

Raw files are not rewritten by maintenance. JSON, Markdown, graph, and embedding writes use temporary files followed by replacement so a process interruption does not normally leave a partial state. Failed URL fetches and failed classifications remain non-fatal and retryable.
