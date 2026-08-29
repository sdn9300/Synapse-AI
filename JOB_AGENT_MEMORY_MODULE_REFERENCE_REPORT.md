# 🧠 SYNAPSE-AI TECHNICAL REFERENCE REPORT
## Architecture Blueprint & Integration Guide for AI Job Agent Architecture (Agent #8: Memory Module)

**Document Version:** 1.0  
**Author:** AI Engineering & Architecture  
**Target Consumer:** AI Native Job Agent Project / Conductor Multi-Agent Ecosystem  
**Mapped Subsystem:** Agent #8 — Persistent Memory & Knowledge Retrieval Subsystem  
**Date:** August 2026  

---

## 1. Executive Summary & Strategic Alignment

### 1.1 The Core Problem in Autonomous Job Search Agents
Autonomous multi-agent job application systems (e.g., **Conductor Multi-Agent Ecosystem**) execute multi-step workflows spanning job harvesting, company intelligence gathering, resume tailoring, automated email outreach, and portal submission. 

However, multi-agent systems without a **stateful, persistent memory module** suffer from severe operational failure modes:
1. **Context Fragmentation & Amnesia:** Each execution run starts from scratch. The system repeats expensive company research, forgets previous recruiter rejections, and fails to compound past interview learnings.
2. **Cold Outreach & Reputation Risk:** Without centralized memory, agents risk re-contacting the same recruiters within short windows, violating cooldown constraints (e.g., 30-day rejection cooldown rules).
3. **Low-Signal Resume Tailoring:** Tailoring engines cannot reference historical resume variations that resulted in positive screening conversion rates.

### 1.2 The Solution: Synapse-AI as Agent #8 (Memory Module)
**Synapse-AI** provides the complete production-proven architectural substrate for **Agent #8 (Memory Module)** in the AI Job Agent Architecture. 

By unifying **immutable raw capture**, **PARA-structured Markdown vaults**, **local vector auto-linking (`[[wikilinks]]`)**, an **interactive knowledge graph**, **grounded RAG search**, and a native **Model Context Protocol (MCP) Tool Server**, Synapse-AI serves as the single source of truth for candidate history, company intelligence, and interaction telemetry.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          CONDUCTOR LANGGRAPH MULTI-AGENT STATEGRAPH                    │
│                                                                                        │
│   ┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐   │
│   │  Harvester  │ ──► │Research Agent│ ──► │ AlignResume  │ ──► │ Overture Outreach│   │
│   └──────┬──────┘     └──────┬───────┘     └──────┬───────┘     └────────┬─────────┘   │
└──────────┼───────────────────┼────────────────────┼──────────────────────┼─────────────┘
           │                   │                    │                      │
           ▼                   ▼                    ▼                      ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   AGENT #8: MEMORY MODULE (SYNAPSE-AI MCP TOOL SERVER)                 │
│                                                                                        │
│   Tools Exposed via JSON-RPC:                                                          │
│   • search_second_brain(query, top_k) ──► Query candidate history & interview notes   │
│   • get_wiki_page(note_id)            ──► Fetch structured company intelligence dossier │
│   • ingest_raw_content(type, content) ──► Store job listings, outreach logs, feedback │
│   • check_cooldown(company_name, days)──► Guard against redundant recruiter outreach  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                           SYNAPSE-AI UNDERLYING STORAGE & AGENTS                       │
│                                                                                        │
│   [raw/] Immutable Capture Store (JD HTML, Email Threads, Recruiter Notes, PDFs)       │
│     │                                                                                  │
│     ▼                                                                                  │
│   [wiki/] AI-Maintained Vault (Projects, Areas, Resources, Archives)                   │
│     │                                                                                  │
│     ├── Local Embeddings (all-MiniLM-L6-v2) ──► Dynamic [[wikilinks]] Auto-Linking    │
│     ├── Vis-Network Knowledge Graph         ──► Entity Relationship Visualization      │
│     ├── Lint & Health Audit Agent (lint.py) ──► Stale Note & Orphan Link Detection     │
│     └── Weekly Digest Agent (digest.py)     ──► Executive Application Pipeline Digest  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Structural & Architectural Mapping (Synapse-AI $\leftrightarrow$ Job Agent)

| Synapse-AI Component | Job Agent Memory Equivalent | Technical Implementation | Value Delivered |
|---|---|---|---|
| **`raw/` Capture Layer** | **Interaction & Artifact Archive** | `capture.py`, `legacy_import.py` | Stores immutable records of raw JDs, recruiter emails, submitted PDF resumes, and interview transcripts with SHA-256 deduplication. |
| **`wiki/Projects/`** | **Active Application Workstreams** | YAML Frontmatter `.md` files | Tracks active job applications (e.g., `Google_FDE_Role.md`, `Stripe_AI_Engineer.md`) with status synced from Conductor. |
| **`wiki/Areas/`** | **Domain & Career Specializations** | YAML Frontmatter `.md` files | Houses skills profiles, target job archetypes, compensation benchmarks, and DevOps/AI engineering roadmaps. |
| **`wiki/Resources/`** | **Company & Market Intelligence** | Auto-scraped company profiles | Detailed dossiers on target companies (tech stack, funding stage, hiring manager profiles, recent news). |
| **`wiki/Archives/`** | **Historical Trails & Rejections** | Rejection cooldown records | Completed or rejected application cycles with post-mortem learnings and timestamped 30-day cooldown timers. |
| **`lib/embeddings.py`** | **Semantic Retrieval Substrate** | `all-MiniLM-L6-v2` (384-dim) | Fast, CPU-friendly dense vector generation enabling sub-100ms similarity scoring over candidate assets without cloud latency. |
| **`link.py` (Auto-Linker)** | **Cross-Entity Relationship Graph** | Cosine Similarity $\ge 0.75$ | Automatically connects job listings to matching resume bullet variations, company tech stacks, and relevant past projects via `[[wikilinks]]`. |
| **`build_graph.py` & UI** | **Application Topology Visualizer** | `vis-network` (Barnes-Hut) | Interactive visualization of target companies, required skills, outreach channels, and application statuses. |
| **`ask.py` (RAG Engine)** | **Grounded Intelligence Synthesizer** | Groq Llama 3.3/3.1 + RAG | Synthesizes grounded candidate answers for custom cover letters, interview Q&A prep, and outreach personalization with source citations. |
| **`mcp_server.py`** | **Agent-to-Agent Interface** | JSON-RPC standard over stdin | Exposes memory capabilities as standardized callable tools for LangGraph Conductor nodes. |
| **`lint.py` (Audit Agent)** | **Pipeline Integrity & Stale Monitor** | Reference & Link Auditor | Detects stale applications (>30 days without update), broken company references, and duplicate job postings. |
| **`digest.py` (Digest Agent)** | **Weekly Application Digest** | Groq Executive Summarizer | Synthesizes weekly pipeline metrics: total applications, outreach sent, interview conversion rates, and skill demand shifts. |

---

## 3. Detailed Data Models & Interface Contracts

### 3.1 Candidate & Interaction Capture Model (`lib/models.py`)

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class JobInteractionMeta:
    """Metadata recorded for every job agent capture in raw/{id}/meta.json."""
    id: str                      # Format: YYYY-MM-DD_{uuid8}
    timestamp: str               # ISO 8601 UTC string
    type: str                    # "job_posting" | "outreach_email" | "interview_note" | "resume_pdf"
    source: str                  # Job board URL, recruiter email, or local path
    company: str                 # e.g., "Databricks"
    role_title: str              # e.g., "Senior AI Engineer"
    content_hash: str            # SHA-256 hash for deduplication (EC-06)
    original_filename: Optional[str] = None

@dataclass
class JobWikiNote:
    """Structured Application / Company note in wiki/ vault."""
    id: str                      # Short note identifier
    raw_id: str                  # Origin raw capture ID
    para: str                    # "Projects" (Active) | "Areas" | "Resources" (Company) | "Archives"
    company: str
    role_title: str
    application_status: str      # "Discovered" | "Tailored" | "Applied" | "Interviewing" | "Rejected" | "Offered"
    tags: List[str]              # ["llm", "rag", "langgraph", "remote"]
    summary: str                 # Executive summary of role/company
    created: str                 # ISO timestamp
    last_contact_date: Optional[str] = None
    links: List[str] = field(default_factory=list)  # Related company / skill note IDs
    body: str = ""               # Full markdown body content
```

### 3.2 Standard Application Frontmatter Schema (`wiki/Projects/{id}.md`)

```yaml
---
id: a1b2c3d4
raw_id: 2026-08-29_a1b2c3d4
para: Projects
company: Databricks
role_title: Senior AI Engineer - Agentic Systems
application_status: Applied
outreach_channel: Overture_Email
recruiter_contact: jane.doe@databricks.com
salary_range: $180k - $220k
tags:
  - agentic-ai
  - langgraph
  - rag
  - distributed-systems
summary: "Senior AI Engineer position on Databricks AI agents platform team."
created: "2026-08-29T10:00:00Z"
last_contact_date: "2026-08-29T10:05:00Z"
cooldown_expires: "2026-09-28T10:05:00Z"
links:
  - comp_databricks
  - skill_langgraph
  - resume_v4_agentic
---

# Role Overview & Tailored Pitch
...
```

---

## 4. Integration Blueprint: Connecting LangGraph Conductor to Synapse-AI

Conductor's multi-agent graph interacts with Synapse-AI at every critical decision boundary:

```
                      ┌────────────────────────────┐
                      │   1. HARVESTER AGENT       │
                      └─────────────┬──────────────┘
                                    │
                        Query MCP: Check deduplication (EC-06)
                                    │
                                    ▼
                      ┌────────────────────────────┐
                      │   2. RESEARCH AGENT        │
                      └─────────────┬──────────────┘
                                    │
                        Query MCP: Fetch cached company intelligence
                        Save MCP: Store newly enriched company dossier
                                    │
                                    ▼
                      ┌────────────────────────────┐
                      │   3. ALIGNRESUME AGENT     │
                      └─────────────┬──────────────┘
                                    │
                        Query MCP: Retrieve highest-converting past bullets
                        Save MCP: Store tailored resume JSON & PDF path
                                    │
                                    ▼
                      ┌────────────────────────────┐
                      │   4. OVERTURE OUTREACH     │
                      └─────────────┬──────────────┘
                                    │
                        Query MCP: Verify 30-day rejection cooldown (EC-07)
                        Save MCP: Log outbound email thread & timestamp
                                    │
                                    ▼
                      ┌────────────────────────────┐
                      │   5. SENTIMENT CLASSIFIER  │
                      └─────────────┬──────────────┘
                                    │
                        Save MCP: Update status ("Interview" / "Rejected")
                        Trigger: If rejected, initiate 30-day cooldown timer
```

### 4.1 Step-by-Step Tool Invocations via MCP

#### Step 1: Pre-Outreach Cooldown Verification (EC-07 Guardrail)
Before dispatching an email or submitting an application, Conductor calls `search_second_brain`:
```json
// Request to MCP Server
{
  "tool": "search_second_brain",
  "args": {
    "query": "What is our interaction history and rejection status with Databricks?",
    "top_k": 3
  }
}

// Response from Synapse-AI MCP
{
  "answer": "Databricks application for AI Infrastructure Role was rejected on 2026-08-10. Active 30-day cooldown is in effect until 2026-09-09. Outreach is currently suppressed.",
  "sources": [
    {
      "id": "app_db_0810",
      "summary": "Databricks application status: Rejected",
      "para": "Archives",
      "relevance_score": 0.882
    }
  ]
}
```

#### Step 2: Ingesting a Newly Discovered Opportunity
When Harvester discovers a new job posting:
```json
// Request to MCP Server
{
  "tool": "ingest_raw_content",
  "args": {
    "content_type": "note",
    "content": "Company: Stripe\nRole: Staff AI Platform Engineer\nURL: https://stripe.com/jobs/123\nRequirements: Python, Distributed Systems, LangGraph, Qdrant.",
    "source_info": "Harvester_LinkedIn_Pipeline"
  }
}

// Response
{
  "status": "success",
  "capture_id": "2026-08-29_f8a9b2c1",
  "classified_para": "Projects",
  "note_id": "f8a9b2c1"
}
```

#### Step 3: Context Retrieval for Tailored Resume Generation
When AlignResume builds a tailored resume for a specific job:
```json
// Request to MCP Server
{
  "tool": "search_second_brain",
  "args": {
    "query": "What are my strongest verified metrics and project bullets for LangGraph multi-agent orchestration and Qdrant vector retrieval?",
    "top_k": 5
  }
}
```

---

## 5. Defensive Guardrails & Edge-Case Architecture

Synapse-AI incorporates robust defensive mechanisms that directly mitigate core job agent risks:

### 5.1 Content Deduplication (EC-06)
- **Problem:** Scrapers frequently encounter duplicate job postings across LinkedIn, Indeed, and company career portals.
- **Solution:** `content_hash()` computes SHA-256 hashes of incoming listings. If an identical JD hash already exists in `raw/`, the system flags the capture, links the new URL to the existing wiki note, and prevents duplicate processing.

### 5.2 Dynamic Rejection Cooldown Loop (EC-07)
- **Problem:** Contacting a company that recently rejected an application damages professional reputation.
- **Solution:** When Sentiment Classifier flags a rejection, the application note is automatically moved to `wiki/Archives/` with frontmatter `cooldown_expires: {date + 30d}`. `link.py` and `mcp_server.py` enforce this barrier before any outbound action.

### 5.3 Offline & Low-Resource Resilience
- **Hardware Profile:** Optimized for 8GB+ RAM local environments.
- **Embeddings:** Kept 100% local via `all-MiniLM-L6-v2` (~80MB RAM footprint). If HuggingFace is offline, a deterministic hash-vector math fallback ensures zero downtime.
- **LLM Failover:** Groq API automatically prioritizes `llama-3.3-70b-versatile` $\rightarrow$ `llama-3.1-8b-instant` $\rightarrow$ heuristic rule-based classification.

---

## 6. Audit & Health Operations (`lint.py` & `digest.py`)

### 6.1 Vault Health Audit (`lint.py`)
Runs on a scheduled cron or post-batch cycle to ensure database integrity:
- **Broken References:** Flags missing target notes in `[[wikilinks]]`.
- **Orphan Job Postings:** Surfaces job listings that have not been linked to any skill or resume variation.
- **Near-Duplicate Detection:** Identifies job listings with $\ge 92\%$ cosine similarity across different job boards.

### 6.2 Weekly Executive Job Search Digest (`digest.py`)
Generates high-level summaries for the candidate:
- **Pipeline Metrics:** Breakdown of active applications in *Projects*, target sectors in *Areas*, company dossiers in *Resources*, and historical records in *Archives*.
- **Market Skill Trends:** LLM-synthesized summary of recurring skill requirements detected across all newly harvested JDs during the week.

---

## 7. Verification & Benchmark Summary

The underlying Synapse-AI engine has been verified with **12 automated unit and integration tests** (`test_secondself.py`) and evaluated using standard **RAGAS retrieval metrics**:

```text
=== SYNAPSE-AI SYSTEM VERIFICATION METRICS ===
• Automated Test Suite: 12/12 Unit & Integration Tests Passed (OK)
• Ingestion Latency: < 1.5 seconds per multi-source capture
• Vector Auto-Linking Threshold: Cosine Similarity >= 0.75
• Broken Reference Rate: 0.0%
• Memory Footprint: ~80MB CPU RAM (Embeddings) + Stateless Cloud LLM (Groq)
• Protocol Standard: Model Context Protocol (MCP) JSON-RPC over stdin/stdout
```

---

## 8. Summary & Next Steps for AI Job Agent Integration

1. **Deploy MCP Server:** Run `python mcp_server.py` as a persistent subprocess or stdio tool inside the Conductor LangGraph environment.
2. **Bind Conductor StateGraph Nodes:** Wire Harvester, Research Agent, AlignResume, and Overture to call `search_second_brain` and `ingest_raw_content`.
3. **Automate Weekly Maintenance:** Schedule `scheduler.py` via cron/Task Scheduler to maintain chronological audit logs in `wiki/log.md`.

*Treat this document as the official Architectural Specification & Integration Reference for Agent #8 (Memory Module) across all future Job Agent development sprints.*
