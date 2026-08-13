# MISSION PLAN & IMPLEMENTATION ROADMAP — SECONDSELF

**Document Version:** 1.0  
**Status:** Approved Mission & Execution Plan  
**System Name:** SecondSelf — Personal AI Second Brain  
**Timeline:** 4-Week Sprint Schedule

---

## 1. Executive Mission & Strategic Alignment

The primary mission of **SecondSelf** is to construct an autonomous, self-organizing knowledge brain that converts raw notes, links, and documents into an organized, connected, and queryable Markdown wiki.

### Roadmap Alignment
* **DevOps Roadmap Capstone (Phase 14):** Satisfies Qdrant vector retrieval, evaluation (RAGAS), and tracing checkpoints using real personal knowledge data instead of synthetic benchmarks.
* **Agentic AI Specialization (Stage 03):** Implements an autonomous ingest/link/lint loop and exposes retrieval as a custom Model Context Protocol (MCP) tool server.
* **AI Job Agent Integration:** Serves as the working prototype for **Memory Module (Agent #8)** in the larger multi-agent job architecture.

---

## 2. Master 4-Week Implementation Roadmap Overview

```
Phase 0: Foundation Setup (Scaffolding, Dependencies, Data Models)
    │
    ▼
Phase 1: The Archivist — Week 1 (Capture Pipeline: Note, Link, File)
    │
    ▼
Phase 2: The Librarian — Week 2 (Sub-Phase 2.1: PARA Classifier | Sub-Phase 2.2: Vector Auto-Linker)
    │
    ▼
Phase 3: The Cartographer — Week 3 (Sub-Phase 3.1: Graph Model | Sub-Phase 3.2: Vis-Network UI)
    │
    ▼
Phase 4: The Oracle — Week 4 (Sub-Phase 4.1: RAG Q&A Engine | Sub-Phase 4.2: Streamlit Deployment)
```

| Phase | Milestone Name | Badge | Primary Deliverables | Checkpoint Output |
|---|---|---|---|---|
| **0** | Foundation Setup | — | Repo scaffold, `requirements.txt`, `lib/models.py`, `lib/storage.py` | Working shared helper library |
| **1** | The Archivist | 🥇 The Archivist | `capture.py` CLI script + 10+ real captured items in `raw/` | `python capture.py` populates `raw/` |
| **2** | The Librarian | 🥇 The Librarian | `classify.py`, `link.py`, `pipeline.py` + 15+ linked notes in `wiki/` | Classified PARA notes with `[[wikilinks]]` |
| **3** | The Cartographer | 🥇 The Cartographer | `build_graph.py`, `data/graph.json`, `static/graph.html` | Force-directed graph view in browser |
| **4** | The Oracle | 🥇 The Oracle | `ask.py`, `app.py`, Streamlit Cloud live deployment URL | Deployed web app with Q&A & graph |

---

## 3. Detailed Phase-by-Phase Task Breakdown

### Phase 0 — Foundation & Repository Setup (Day 0)
* **Goal:** Scaffold the repository structure and implement foundational data models and storage helpers.
* **Tasks:**
  1. Create directory tree:
     * `raw/`
     * `wiki/{Projects, Areas, Resources, Archives}/`
     * `data/`, `lib/`, `static/`
  2. Create `requirements.txt`:
     ```text
     streamlit>=1.32
     groq>=0.4
     sentence-transformers>=2.3
     numpy>=1.24
     pyyaml>=6.0
     pypdf>=4.0
     requests>=2.31
     beautifulsoup4>=4.12
     python-dotenv>=1.0
     ```
  3. Implement `lib/models.py` defining `CaptureMeta`, `CaptureResult`, `WikiNote`, `GraphNode`, `GraphEdge`, and `AskResult`.
  4. Implement `lib/storage.py` providing `generate_capture_id()`, `write_raw_capture()`, `read_raw_captures()`, `write_wiki_note()`, `read_wiki_notes()`, `load_index()`, `save_index()`, and `content_hash()`.
  5. Initialize `data/index.json` with `{"raw_processed": {}, "embeddings_version": "all-MiniLM-L6-v2", "last_graph_build": null}`.
* **Verification:** `python -c "from lib import models, storage"` executes cleanly without import errors.

---

### Phase 1 — The Archivist: Multi-Source Capture Pipeline (Week 1)
* **Goal:** Create a single command-line interface that captures notes, links, or files into `raw/` with unique IDs and ISO timestamps.
* **Tasks:**
  1. Implement `capture.py` core functions:
     * `capture_note(text: str) -> CaptureResult`
     * `capture_link(url: str, notes: str = "") -> CaptureResult`
     * `capture_file(path: str) -> CaptureResult`
  2. Implement CLI interface using `argparse`:
     * `python capture.py note "Idea text"`
     * `python capture.py link "https://example.com"`
     * `python capture.py file "./document.pdf"`
     * `python capture.py` (interactive stdin mode)
  3. Handle edge cases: missing files (exit error), empty text (reject with warning), duplicate content (SHA-256 warning but allow capture), binary file handling.
  4. Ingest at least 10 real pieces of user information (4 text notes, 3 bookmarks, 3 local files).
* **Acceptance Criteria:**
  * [x] `raw/` and `wiki/` directory structures exist.
  * [x] One command captures a note, a link, and a file.
  * [x] Every capture creates `raw/{id}/meta.json` with timestamp and unique ID.
  * [x] 10+ real items ingested.

---

### Phase 2 — The Librarian: Classification & Auto-Linking (Week 2)

#### Sub-Phase 2.1 — Auto-Classify (Days 1–3)
* **Tasks:**
  1. Set up Groq API key in `.env` (`GROQ_API_KEY=...`).
  2. Implement `lib/llm.py`:
     * `call_llm(prompt, system)` wrapper with retry logic using `llama-3.1-8b-instant`.
     * `classify_content(text)` returning structured JSON `{para, tags, summary}`.
  3. Implement text extraction helpers for web links (BeautifulSoup4) and PDFs (PyPDF).
  4. Implement `classify.py`:
     * Iterates over unprocessed items in `data/index.json`.
     * Extracts text $\rightarrow$ calls `classify_content()` $\rightarrow$ writes `wiki/{para}/{id}.md` with YAML frontmatter.
     * Updates `data/index.json`.

#### Sub-Phase 2.2 — Auto-Link Related Notes (Days 4–7)
* **Tasks:**
  1. Implement `lib/embeddings.py`:
     * `load_model()` caching `all-MiniLM-L6-v2`.
     * `embed_text(text)` returning 384-dim vector.
     * `cosine_similarity(a, b)` computing similarity score.
  2. Implement `link.py`:
     * Computes embeddings for all wiki notes (`title + summary + body`).
     * Compares new note embeddings against existing vectors in `data/embeddings.pkl`.
     * If Cosine Similarity $\ge 0.75$, updates frontmatter `links: []` and appends `[[target-id]]` to body text.
  3. Implement `pipeline.py` orchestrator:
     * `python pipeline.py classify`
     * `python pipeline.py link`
     * `python pipeline.py process` (runs classify + link sequentially).
* **Acceptance Criteria:**
  * [x] Auto-classification assigns valid PARA category, tags, and summary.
  * [x] Embeddings computed and cached in `data/embeddings.pkl`.
  * [x] Related notes auto-linked with `[[wikilinks]]` without manual tagging.
  * [x] Pipeline executed over 15+ real items.

---

### Phase 3 — The Cartographer: Knowledge Graph Visualization (Week 3)

#### Sub-Phase 3.1 — Graph Data Model (Days 1–3)
* **Tasks:**
  1. Implement `build_graph.py`:
     * Parses all `wiki/**/*.md` files.
     * Generates nodes (`id`, `label`, `para`, `tags`, `summary`, `content_preview`, `group`).
     * Extracts links from YAML frontmatter and body wikilinks $\rightarrow$ generates deduplicated edges (`source`, `target`, `weight`, `type`).
     * Exports structured payload to `data/graph.json`.

#### Sub-Phase 3.2 — Interactive Graph Interface (Days 4–7)
* **Tasks:**
  1. Create `static/graph.html` using `vis-network` (v9.1+):
     * Loads `data/graph.json`.
     * Configures force-directed physics layout (Barnes-Hut: `gravitationalConstant: -8000`, `springLength: 150`).
     * Colors nodes dynamically by PARA group.
     * Implements hover tooltips (revealing summary & content preview) and drag-to-explore/zoom interactions.
  2. Integrate `build_graph.py` into `pipeline.py process` so graph data auto-rebuilds after processing new captures.
* **Acceptance Criteria:**
  * [x] `build_graph.py` exports clean `data/graph.json`.
  * [x] Interactive force-directed network graph renders in browser.
  * [x] Node hover reveals note summaries and content preview.
  * [x] Dragging, zooming, and node pulsing operate smoothly.

---

### Phase 4 — The Oracle: Ask Your Brain & Deployment (Week 4)

#### Sub-Phase 4.1 — Natural Language Search Engine (Days 1–3)
* **Tasks:**
  1. Implement `ask.py`:
     * `ask(question: str, top_k: int = 5) -> AskResult`.
     * Pipeline: Embed question $\rightarrow$ Rank top-$K$ notes by cosine similarity from `data/embeddings.pkl` $\rightarrow$ Load full wiki bodies $\rightarrow$ Construct RAG prompt $\rightarrow$ Call Groq LLM `synthesize_answer()` $\rightarrow$ Return synthesized answer and citations.
  2. Guardrails: Set temperature to `0.3`, truncate context to ~6000 tokens, return fallback message "I don't have notes about that" if top similarity score is below threshold ($0.4$).

#### Sub-Phase 4.2 — Streamlit App & Cloud Deployment (Days 4–7)
* **Tasks:**
  1. Implement `app.py`:
     * Header & status stats.
     * Natural language search bar + answer synthesis display with source cards.
     * Embedded interactive graph via `st.components.v1.html(..., height=550)`.
     * Sidebar form supporting note capture, link capture, file upload, and `[Process Pipeline]` trigger button.
     * Performance caching via `@st.cache_resource` and `@st.cache_data`.
  2. Write `README.md` with setup instructions, architecture overview, and command reference.
  3. Deploy to Streamlit Community Cloud (connected to GitHub repository with `GROQ_API_KEY` added to Secrets).
* **Acceptance Criteria:**
  * [x] `ask()` synthesizes answers citing source notes `[note-id]`.
  * [x] Unified Streamlit app integrates search bar, graph view, and capture forms.
  * [x] App deployed and verified on public cloud URL.

---

## 4. Risk Register & Mitigation Strategy

| Risk Scenario | Severity | Mitigation Strategy | Fallback Mechanism |
|---|---|---|---|
| **Groq API Rate Limits / Failure** | Medium | Batch classification calls; implement exponential backoff retry in `lib/llm.py`. | Fallback to raw capture storage without blocking pipeline. |
| **Embedding Model Cold-Start** | Low | Pre-load `SentenceTransformer` with `@st.cache_resource` in Streamlit. | Display st.spinner while loading model weights. |
| **Cluttered Graph Visualization** | Medium | Filter nodes by PARA category in UI; set minimum weight threshold for edges ($0.75$). | Provide group toggle checkboxes in `graph.html`. |
| **PDF Extraction Failure** | Low | Wrap PyPDF extraction in try-except block. | Fallback to extracting document filename & raw metadata. |
| **Private Notes Security** | High | Separate `raw/` into `public/` and `private/` tiers in schema before cloud LLM ingest. | Route `private/` tier through local embedding/LLM. |
| **Streamlit Iframe Sizing** | Low | Set explicit pixel height (`height=550`) on `st.components.v1.html`. | Provide full-screen expansion link for graph HTML. |
