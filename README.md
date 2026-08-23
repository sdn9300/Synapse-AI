# 🧠 Synapse-AI — Personal AI Second Brain & Knowledge Graph

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Groq Llama 3](https://img.shields.io/badge/LLM-Groq%20Llama%203.3-green.svg)](https://console.groq.com/)
[![Embeddings](https://img.shields.io/badge/Embeddings-SentenceTransformers-orange.svg)](https://huggingface.co/sentence-transformers)
[![Tests](https://img.shields.io/badge/tests-12%20passed-brightgreen.svg)](test_secondself.py)

**Synapse-AI** is a local-first **Personal AI Second Brain** and Karpathy-pattern **LLM Wiki**. It captures notes, web bookmarks, Obsidian inbox entries, and documents, automatically categorizes them using the PARA method (*Projects, Areas, Resources, Archives*), auto-links related concepts with 384-dimensional local vector embeddings, renders an interactive force-directed knowledge graph, and provides Retrieval-Augmented Generation (RAG) natural language search over your accumulated knowledge.

---

## 🌟 Key Features

1. **Multi-Source Capture & Obsidian Inbox Integration:** Single-command CLI or web form capture for text notes, URLs, and local files (PDFs, Markdown, text), plus automated ingestion from `wiki/Inbox/`.
2. **Immutable Raw Storage:** Source records land in `raw/{id}/meta.json` with ISO timestamps, UUIDs, and SHA-256 deduplication hashes.
3. **Automated AI Librarian & Frontmatter Normalization:** AI processing loop classifies raw captures into PARA folders (`wiki/Projects`, `wiki/Areas`, `wiki/Resources`, `wiki/Archives`) with structured YAML frontmatter and support for custom index overrides.
4. **Local Vector Auto-Linking:** Local `sentence-transformers` (`all-MiniLM-L6-v2`) compute cosine similarity matrix ($\ge 0.75$) and automatically insert `[[wikilinks]]` cross-references.
5. **Interactive Knowledge Graph:** HTML5 `vis-network` force-directed graph viewer with color-coded PARA nodes, hover tooltips, drag-to-explore, and zoom.
6. **Ask-Your-Brain RAG Search Engine:** Natural language Q&A synthesizing answers strictly grounded in retrieved note contexts with source citations powered by Groq Llama 3.3 / Llama 3.1 with model failover.
7. **Model Context Protocol (MCP) Tool Server:** Exposes custom MCP tools (`search_second_brain`, `get_wiki_page`, `ingest_raw_content`) for external AI agents (Conductor, Antigravity, etc.).
8. **Vault Health & Lint Agent:** `lint.py` audits broken `[[wikilinks]]`, orphan pages, and near-duplicate notes $\rightarrow$ outputs `wiki/synthesis/health_report.md`.
9. **Weekly Executive Synthesis Agent:** `digest.py` synthesizes weekly executive reports $\rightarrow$ outputs `wiki/synthesis/YYYY-Www.md`.
10. **Legacy Batch Importer & Standing Maintenance Scheduler:** `legacy_import.py` for recursive folder imports and `scheduler.py` for automated audit logging in `wiki/log.md`.
11. **Automated Test Suite:** 12 automated unit and integration tests (`test_secondself.py`) covering all core subsystems.

---

## 📁 Repository Structure

```
Synapse-AI/
├── raw/                         # Immutable raw capture store
├── wiki/                        # AI-maintained markdown knowledge vault & Obsidian vault
│   ├── Projects/
│   ├── Areas/
│   ├── Resources/
│   ├── Archives/
│   ├── Inbox/                   # Obsidian note staging inbox
│   └── synthesis/               # Weekly digests & health audit reports
├── data/                        # State index, embeddings, and graph payload
│   ├── index.json
│   ├── embeddings.pkl
│   └── graph.json
├── lib/                         # Core module package
│   ├── models.py                # Dataclasses & schemas
│   ├── storage.py               # File system helpers & JSON IO
│   ├── llm.py                   # Groq API client with model failover
│   ├── markdown.py              # Frontmatter stripping & normalization
│   └── embeddings.py            # SentenceTransformers wrapper & vector math
├── static/                      # Static web assets
│   └── graph.html               # vis-network interactive graph UI
├── capture.py                   # CLI capture pipeline
├── obsidian_inbox.py            # Obsidian Inbox staging importer
├── classify.py                  # Raw-to-wiki classifier
├── link.py                      # Embedding auto-linker
├── pipeline.py                  # Master pipeline orchestrator
├── build_graph.py               # Graph JSON generator
├── ask.py                       # RAG Q&A search engine
├── app.py                       # Unified Streamlit web application
├── mcp_server.py                # Model Context Protocol tool server
├── lint.py                      # Vault health audit agent
├── digest.py                    # Weekly synthesis digest agent
├── legacy_import.py             # Batch document importer
├── scheduler.py                 # Standing maintenance scheduler
├── eval_benchmark.py            # Quality evaluation benchmark suite
├── test_secondself.py           # Automated unit & integration test suite
├── PROBLEM_STATEMENT.md         # Detailed problem statement specification
├── ARCHITECTURE.md              # Technical architecture documentation
├── MISSION_PLAN.md              # Milestone execution roadmap
├── IMPLEMENTATION_PLAN.md       # 10-phase build guide
├── EVALUATION_PLAN.md           # RAGAS evaluation plan
├── EDGE_CASE_PLAN.md            # Edge-case handling plan
├── SCHEMA.md                    # System conventions & frontmatter standard
└── requirements.txt             # Dependencies
```

---

## 🚀 Quickstart Guide

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional)
Copy `.env.example` to `.env` and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```
*(Note: Synapse-AI includes heuristic fallback classification and local vector math, allowing the system to run locally even without an API key).*

### 3. Ingest & Capture Content
```bash
# Capture a text note
python capture.py note "DevOps Phase 14 capstone focuses on Qdrant and RAGAS."

# Capture a web link
python capture.py link "https://huggingface.co/sentence-transformers" --notes "Local embedding model"

# Capture a local file
python capture.py file "./ARCHITECTURE.md"

# Import a folder of legacy documents
python legacy_import.py "./path/to/my_notes"
```

### 4. Process Knowledge Pipeline
```bash
# Ingest Obsidian Inbox + Classify + Auto-link + Rebuild Graph
python pipeline.py process
```

### 5. Query Natural Language Search
```bash
python ask.py "What is Synapse-AI and what are its core goals?"
```

### 6. Run Agents & Test Suite
```bash
# Run Vault Health & Lint Agent
python lint.py

# Run Weekly Executive Digest Agent
python digest.py

# Run Automated Unit & Integration Tests
python -m unittest test_secondself.py

# Run Quality Evaluation Benchmark Suite
python eval_benchmark.py
```

### 7. Launch Web UI & MCP Tool Server
```bash
# Launch Streamlit Web UI Dashboard
streamlit run app.py

# Query via MCP Tool Server
python mcp_server.py --tool search_second_brain --query "What is Synapse-AI?"
```

---

## 📄 Documentation Links

- [PROBLEM_STATEMENT.md](file:///c:/My%20Projects/Masai%20Live%20Docs/Second_Brain/PROBLEM_STATEMENT.md) — Detailed problem statement, goals, scope, and criteria.
- [ARCHITECTURE.md](file:///c:/My%20Projects/Masai%20Live%20Docs/Second_Brain/ARCHITECTURE.md) — System architecture, data schemas, and pipeline designs.
- [MISSION_PLAN.md](file:///c:/My%20Projects/Masai%20Live%20Docs/Second_Brain/MISSION_PLAN.md) — 4-week execution roadmap, milestones, and risk register.
- [IMPLEMENTATION_PLAN.md](file:///c:/My%20Projects/Masai%20Live%20Docs/Second_Brain/IMPLEMENTATION_PLAN.md) — 10-phase engineering build plan.
- [EVALUATION_PLAN.md](file:///c:/My%20Projects/Masai%20Live%20Docs/Second_Brain/EVALUATION_PLAN.md) — RAGAS evaluation plan & quality metrics.
- [EDGE_CASE_PLAN.md](file:///c:/My%20Projects/Masai%20Live%20Docs/Second_Brain/EDGE_CASE_PLAN.md) — Defensive edge-case matrix.
- [SCHEMA.md](file:///c:/My%20Projects/Masai%20Live%20Docs/Second_Brain/SCHEMA.md) — Vault conventions and Markdown frontmatter standard.
