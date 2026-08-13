# SCHEMA.md — Second Brain Conventions

## Folder Organization (PARA Method)
- `raw/`: Immutable source of truth — captured notes, links, dropped files. Agent reads, never edits.
- `wiki/Projects/`: YOUR active projects specifically (e.g. AlignResume, Gleaner, Conductor, SecondSelf).
- `wiki/Areas/`: Ongoing responsibilities and domains (e.g. DevOps, Agentic AI, Career).
- `wiki/Resources/`: Reference materials, external articles, tutorials, repositories.
- `wiki/Archives/`: Completed, inactive, or archived topics.

## Page Types & Frontmatter Standards
Each wiki page is formatted as Markdown with YAML frontmatter:

```yaml
---
id: a1b2c3d4
raw_id: 2026-08-02_a1b2c3d4
para: Projects
tags: [ml, agent, architecture]
summary: "One-line executive summary of the note."
created: 2026-08-02T20:10:00Z
links: ["e5f6g7h8", "i9j0k1l2"]
---
```

## Ingest & Auto-Link Workflow
1. Read unprocessed folders in `raw/` not yet in `data/index.json`.
2. Extract text and send to Groq LLM classifier (`llama-3.1-8b-instant`).
3. Save structured markdown file to `wiki/{para}/{id}.md`.
4. Compute local embeddings (`all-MiniLM-L6-v2`) and compare against all existing wiki vectors.
5. If similarity $\ge 0.75$, add target ID to `links: []` frontmatter and append `[[target-id]]` to body.
6. Rebuild `data/graph.json` for `vis-network` interactive graph view.
