# PHASE-WISE IMPLEMENTATION PLAN — SECONDSELF

**Document Version:** 2.0  
**Status:** Approved Execution Plan  
**System Name:** SecondSelf Personal AI Second Brain  
**Structure:** 10-Phase Detailed Engineering Build Plan (Phase 0 through Phase 9)

---

## 1. Executive Implementation Overview

This document outlines the step-by-step phase-wise build guide for **SecondSelf**, expanding the curriculum roadmap into 10 explicit, testable engineering phases. Each phase is self-contained, tested on real user data, and produces a concrete working checkpoint that feeds directly into subsequent phases.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 PHASE 0: SETUP & SCAFFOLD                              │
│  Directory Structure (raw/, wiki/, data/, lib/, static/) + Dependencies & Environment  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              PHASES 1 - 5: CODE IMPLEMENTATION                         │
│  Phase 1: Multi-Source Capture CLI (capture.py)                                       │
│  Phase 2: Text Extraction & Normalization (HTML/PDF/Text)                              │
│  Phase 3: PARA LLM Classifier & Markdown Vault (classify.py)                          │
│  Phase 4: Local Vector Embeddings & Auto-Linker (link.py)                              │
│  Phase 5: Knowledge Graph Builder & vis-network UI (build_graph.py + static/graph.html)│
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              PHASES 6 - 7: LOCAL TESTING & RAG                         │
│  Phase 6: Natural Language RAG Search Engine (ask.py)                                  │
│  Phase 7: Streamlit Web UI Integration & Local E2E Verification (app.py)               │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          PHASES 8 - 9: DEPLOYMENT & VERIFICATION                       │
│  Phase 8: Streamlit Cloud / HF Spaces Deployment & Secrets Configuration               │
│  Phase 9: Final Quality Assurance, Evaluation Benchmarks & Documentation               │
└───────────────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 2. Phase-by-Phase Technical Build Plan

### Phase 0 — Foundation & Repository Setup (Day 0)
* **Objective:** Scaffold the workspace directory structure, environment variables, shared data models, and storage helper functions.
* **Tasks:**
  - Create directory layout:
    ```
    secondself/
    ├── raw/
    ├── wiki/
    │   ├── Projects/
    │   ├── Areas/
    │   ├── Resources/
    │   └── Archives/
    ├── data/
    ├── lib/
    └── static/
    ```
  - Create `requirements.txt` (`streamlit`, `groq`, `sentence-transformers`, `numpy`, `pyyaml`, `pypdf`, `requests`, `beautifulsoup4`, `python-dotenv`).
  - Create `.env.example` and `.gitignore`.
  - Implement `lib/models.py` (`CaptureMeta`, `CaptureResult`, `WikiNote`, `GraphNode`, `GraphEdge`, `AskResult`).
  - Implement `lib/storage.py` (`generate_capture_id`, `write_raw_capture`, `read_raw_captures`, `write_wiki_note`, `read_wiki_notes`, `load_index`, `save_index`).
  - Initialize `data/index.json`.
* **Ship Checkpoint:** Clean execution of `python -c "from lib import models, storage"`.

---

### Phase 1 — Multi-Source Capture Pipeline (Week 1)
* **Objective:** Build a single CLI interface that captures text notes, web URLs, and local files into immutable `raw/{id}/` storage.
* **Tasks:**
  - Implement `capture.py` core functions: `capture_note()`, `capture_link()`, `capture_file()`.
  - Implement `argparse` CLI sub-commands: `note`, `link`, `file`, and fallback interactive mode.
  - Implement SHA-256 content hashing to warn on duplicate captures.
  - Record ISO timestamps and unique IDs (`YYYY-MM-DD_{uuid8}`).
  - Test capture pipeline by ingesting 10+ real pieces of user content into `raw/`.
* **Ship Checkpoint:** `python capture.py note "..."`, `python capture.py link "..."`, `python capture.py file "..."` successfully populate `raw/`.

---

### Phase 2 — Text Extraction & Content Normalization (Week 2.1a)
* **Objective:** Build robust text extraction routines for multi-format content.
* **Tasks:**
  - Plain text / Markdown: read text directly.
  - Web URLs: execute HTTP GET requests, clean HTML nav/script tags using `BeautifulSoup4`, and extract clean body text. Fallback to raw link string on failure.
  - Local PDFs: parse pages using `pypdf.PdfReader` (extracting text from first 10 pages). Fallback to filename on failure.
  - Binary/Other files: record original filename in metadata.
* **Ship Checkpoint:** `extract_text_from_raw()` extracts clean text across test notes, URLs, and PDFs without crashing.

---

### Phase 3 — PARA Classification & Wiki Vault Generation (Week 2.1b)
* **Objective:** Implement LLM classifier to organize raw captures into PARA markdown notes.
* **Tasks:**
  - Implement `lib/llm.py` Groq API client (`llama-3.1-8b-instant`) with heuristic fallback classifier.
  - Instruct LLM to return strict JSON payload: `{"para": "Projects|Areas|Resources|Archives", "tags": [...], "summary": "..."}`.
  - Implement `classify.py` to process unindexed items in `data/index.json`.
  - Save structured Markdown pages to `wiki/{para}/{id}.md` with YAML frontmatter headers.
* **Ship Checkpoint:** `python classify.py` generates organized `.md` files under `wiki/Projects`, `wiki/Areas`, `wiki/Resources`, `wiki/Archives`.

---

### Phase 4 — Local Vector Embeddings & Auto-Linking (Week 2.2)
* **Objective:** Compute 384-dimensional embeddings and auto-insert cross-reference links between related notes.
* **Tasks:**
  - Implement `lib/embeddings.py` using `sentence-transformers/all-MiniLM-L6-v2` and numpy cosine similarity math.
  - Implement `link.py` to compare vector similarity across all note pairs.
  - If Cosine Similarity $\ge 0.75$:
    - Append target ID to frontmatter `links: []`.
    - Append inline wikilink `[[target-id]]` to note body.
  - Save computed vectors to `data/embeddings.pkl`.
  - Implement `pipeline.py` orchestrator (`python pipeline.py process`).
* **Ship Checkpoint:** `python pipeline.py process` executes classification and auto-linking, inserting `[[wikilinks]]`.

---

### Phase 5 — Knowledge Graph Builder & vis-network UI (Week 3)
* **Objective:** Build graph JSON payload and render an interactive force-directed network graph in browser.
* **Tasks:**
  - Implement `build_graph.py` to parse all `wiki/**/*.md` files, extract nodes/edges, deduplicate links, and export `data/graph.json`.
  - Create `static/graph.html` using `vis-network` (v9.1+ CDN).
  - Configure Barnes-Hut physics layout (`gravitationalConstant: -7000`, `centralGravity: 0.3`, `springLength: 140`).
  - Color-code nodes by PARA group (Projects: Green, Areas: Blue, Resources: Orange, Archives: Gray).
  - Implement hover tooltips (showing title, summary, content preview) and drag/zoom interactions.
* **Ship Checkpoint:** `python build_graph.py` generates `data/graph.json` and renders interactive graph at `http://localhost:8000/static/graph.html`.

---

### Phase 6 — Natural Language RAG Q&A Engine (Week 4.1)
* **Objective:** Build natural language search engine answering questions grounded in personal notes.
* **Tasks:**
  - Implement `ask.py`: `ask(question: str, top_k: int = 5) -> AskResult`.
  - Vector search: embed question $\rightarrow$ rank top-$K$ notes by cosine similarity $\rightarrow$ load note bodies $\rightarrow$ format context prompt.
  - Call Groq LLM `synthesize_answer()` with temperature `0.3`.
  - Guardrails: return fallback message ("I don't have notes about that") if top similarity is below $0.15$.
  - Citation formatting: append inline source citations `[note-id]`.
* **Ship Checkpoint:** `python ask.py "What are my core goals?"` outputs synthesized answer with cited sources.

---

### Phase 7 — Unified Streamlit App & Local Testing (Week 4.2a)
* **Objective:** Assemble Q&A search, graph view, and capture forms into a unified Streamlit UI and perform local E2E testing.
* **Tasks:**
  - Implement `app.py`:
    - Top header & vault metrics banner (Raw captures, Wiki pages, Graph nodes, Auto-links).
    - Ask bar + answer display with source card expanders.
    - Embedded `vis-network` graph via `st.components.v1.html()`.
    - Sidebar tabs for Note capture, Link capture, File upload, and `[Process Pipeline]` trigger button.
    - Performance caching via `@st.cache_data` and `@st.cache_resource`.
  - Test local execution via `streamlit run app.py`.
* **Ship Checkpoint:** Local Streamlit application loads cleanly at `http://localhost:8501`.

---

### Phase 8 — Cloud Deployment & Environment Configuration (Week 4.2b)
* **Objective:** Deploy SecondSelf to a public cloud platform (Streamlit Community Cloud / Hugging Face Spaces).
* **Tasks:**
  - Push repository to public/private GitHub repository.
  - Connect repository to Streamlit Cloud (`share.streamlit.io`).
  - Configure `GROQ_API_KEY` in Streamlit Secrets.
  - Pre-commit sample `wiki/`, `data/graph.json`, and `data/embeddings.pkl` to demonstrate public functionality out-of-the-box.
* **Ship Checkpoint:** Live public Streamlit URL (e.g. `https://secondself.streamlit.app`) loads and executes end-to-end.

---

### Phase 9 — Final Quality Assurance, Benchmarks & Documentation
* **Objective:** Run end-to-end integration tests, verify quality benchmarks, and finalize repository documentation.
* **Tasks:**
  - Run full E2E verification flow: Capture new item $\rightarrow$ Process pipeline $\rightarrow$ Verify graph update $\rightarrow$ Ask question $\rightarrow$ Check source citations.
  - Verify acceptance criteria across all 4 weekly milestones.
  - Finalize `README.md`, `PROBLEM_STATEMENT.md`, `ARCHITECTURE.md`, `MISSION_PLAN.md`, `SCHEMA.md`, and `EVALUATION_PLAN.md`.
* **Ship Checkpoint:** Clean git repository with 100% verified test checkpoints.
