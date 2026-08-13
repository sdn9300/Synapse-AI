# 🧠 Synapse-AI — Personal AI Second Brain & Knowledge Graph

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Groq Llama 3](https://img.shields.io/badge/LLM-Groq%20Llama%203-green.svg)](https://console.groq.com/)
[![Embeddings](https://img.shields.io/badge/Embeddings-SentenceTransformers-orange.svg)](https://huggingface.co/sentence-transformers)

**Synapse-AI** is a local-first **Personal AI Second Brain** and Karpathy-pattern **LLM Wiki**. It captures notes, web bookmarks, and documents, automatically categorizes them using the PARA method (*Projects, Areas, Resources, Archives*), auto-links related concepts with 384-dimensional local vector embeddings, renders an interactive force-directed knowledge graph, and provides Retrieval-Augmented Generation (RAG) natural language search over your accumulated knowledge.

---

## 🌟 Key Features

1. **Multi-Source Capture:** Single-command CLI or web form capture for text notes, URLs, and local files (PDFs, Markdown, text).
2. **Immutable Raw Storage:** Source records land in `raw/{id}/meta.json` with ISO timestamps, UUIDs, and SHA-256 deduplication hashes.
3. **Automated AI Librarian:** AI processing loop classifies raw captures into PARA folders (`wiki/Projects`, `wiki/Areas`, `wiki/Resources`, `wiki/Archives`) with structured YAML frontmatter.
4. **Local Vector Auto-Linking:** Local `sentence-transformers` (`all-MiniLM-L6-v2`) compute cosine similarity matrix ($\ge 0.75$) and automatically insert `[[wikilinks]]` cross-references.
5. **Interactive Knowledge Graph:** HTML5 `vis-network` force-directed graph viewer with color-coded PARA nodes, hover tooltips, drag-to-explore, and zoom.
6. **Ask-Your-Brain RAG Search Engine:** Natural language Q&A synthesizing answers strictly grounded in retrieved note contexts with source citations.
7. **MCP Tool Server:** Model Context Protocol tool server (`search_second_brain`, `get_wiki_page`, `ingest_raw_content`) for external AI agents.

---

## 📁 Repository Structure

```
Synapse-AI/
├── raw/                         # Immutable raw capture store
├── wiki/                        # AI-maintained markdown knowledge vault
│   ├── Projects/
│   ├── Areas/
│   ├── Resources/
│   └── Archives/
├── data/                        # State index, embeddings, and graph payload
│   ├── index.json
│   ├── embeddings.pkl
│   └── graph.json
├── lib/                         # Core module package
│   ├── models.py                # Dataclasses & schemas
│   ├── storage.py               # File system helpers & JSON IO
│   ├── llm.py                   # Groq API client & heuristic classifier
│   └── embeddings.py            # SentenceTransformers wrapper & vector math
├── static/                      # Static web assets
│   └── graph.html               # vis-network interactive graph UI
├── capture.py                   # CLI capture pipeline
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
├── test_secondself.py           # Automated unit test suite
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
*(Note: Synapse-AI includes a heuristic fallback classifier and local embedding module, allowing the system to run locally even without an API key).*

### 3. Capture Content
```bash
# Capture a text note
python capture.py note "DevOps Phase 14 capstone focuses on Qdrant and RAGAS."

# Capture a web link
python capture.py link "https://huggingface.co/sentence-transformers" --notes "Local embedding model"

# Capture a local file
python capture.py file "./ARCHITECTURE.md"
```

### 4. Process Knowledge Pipeline
```bash
# Run classification + auto-linking + graph building sequentially
python pipeline.py process
```

### 5. Query Natural Language Search
```bash
python ask.py "What is Synapse-AI and what are its core goals?"
```

### 6. Launch Web UI
```bash
streamlit run app.py
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
