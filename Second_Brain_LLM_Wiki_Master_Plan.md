UNIFIED PERSONAL AI SECOND BRAIN
Local Document/Notes System + Karpathy-Pattern LLM Wiki
Master Architecture & Execution Plan

Compiled: July 2026
Companion to: SDN_Mission_Plan v1.2, Part I (Skills/Identity), Part II (Projects/Career)
Status: Pre-implementation — architecture document, no code yet
Document type: Spec-Anchored (per your SDD standard — this evolves with the build)
Document version: 1.2

Revision log:
- v1.0 — Initial architecture: raw/wiki/schema layers, module breakdown, 6-phase roadmap, open questions on inference provider, existing notes, agent runtime.
- v1.1 — Resolved all three v1.0 open questions: provider abstraction (§9.7) for Groq-now/Ollama-later with permanently local embeddings; added Phase 0.5 Legacy Consolidation for Android/computer/Drive notes via Google Drive API; confirmed pure-Python agent runtime, Claude Code decided against (§9.6).
- v1.2 — Split §9.6 into two separate decisions: what executes continuously at runtime (unchanged — pure Python + Groq) vs. what helps write that code (Claude Code, Antigravity, and Codex now explicitly in provision, matching the AI-assisted-construction pattern already used on AlignResume/Overture/Gleaner). Added an interview-readiness risk entry mirroring the same flag already in the Job Prep doc.

---

## 1. Executive Summary

Two requests, one system. You asked for (a) a local database/document store where your notes, learning materials, and personal documents get maintained by AI agents, and (b) a Karpathy-pattern "LLM Wiki" second brain that captures everything you read and watch. These are not two projects — they are one system with two intake channels feeding the same underlying structure.

The strategic case for building this now, specifically:

- It **is** the DevOps roadmap's Phase 14 capstone (Qdrant + RAGAS + tracing), brought forward and given a real, personally-motivating use case instead of a synthetic checkpoint.
- It **is** the Stage 03 "Agentic AI Mastery" specialization in miniature: an ingest/link/lint/digest agent loop, an MCP server exposing retrieval as a tool, and eventually a supervisor pattern — the exact skill stack that phase already targets.
- It **becomes** the working prototype for Memory Module (Agent #8) in the AI Job Agent Architecture — same infrastructure (persistent, queryable memory), different content domain.
- It directly replaces the manual maintenance burden behind your own "Living Notes" update log (Part I, §13) — the Mission Plan, Skills Profile, and Job Prep docs are themselves exactly the kind of content this system is built to keep current without hand-editing.

One build satisfies four separate line items already on your roadmap. That overlap is the justification for prioritizing it — not a parallel commitment competing for the same hours.

---

## 2. Problem Statement

Two concrete, currently-unsolved problems:

1. **Personal documents decay through manual maintenance.** Your Mission Plan, Skills Profile, and project docs are accurate today because you (or a chat session) hand-update them. There is no standing mechanism that notices "Conductor's status changed" or "a new project shipped" and updates the record on its own. The document's freshness is bounded by how often you remember to edit it.
2. **Consumed content leaves no durable trace.** Articles read and videos watched currently vanish into browser history and memory. Nothing connects "the RAG tutorial I watched in March" to "the Qdrant capstone I'm building in October," even though they're the same topic. Knowledge doesn't compound — it resets with every new source.

Why it matters: you're already running a disciplined, multi-year, evidence-based career plan. The raw material for that plan's next five years — everything you read, watch, and build — is currently the least-structured part of the entire operation.

---

## 3. Project Goals

| # | Goal | Measurable target |
|---|---|---|
| G1 | Personal docs/notes stay current without manual re-editing | New project status changes reflected in wiki within 1 ingest cycle, not next chat session |
| G2 | Articles/videos become linked, summarized, findable | Every source produces a wiki page within 48h of capture |
| G3 | System answers "what do I know about X" | Query returns a synthesized answer citing specific wiki pages, not raw search results |
| G4 | Reuses existing roadmap infrastructure | Phase 14 (Qdrant/RAGAS) and Stage 03 (MCP) checkpoints satisfied by this build, not duplicated later |
| G5 | Local-first | Raw content + wiki live on your machine / a private git repo; only inference calls leave it |

---

## 4. Scope Definition

**In scope (MVP + near-term):**
- Markdown-based vault: `raw/` (immutable sources) → `wiki/` (AI-maintained pages) → schema file (conventions)
- Capture: personal docs/notes (PDF, docx, md, txt), web articles, YouTube video transcripts
- Agent operations: ingest, link, lint (health-check), digest (weekly synthesis)
- Git version history (you already use this daily — zero new tooling)
- Vector search + RAGAS eval layer once the vault outgrows Obsidian's native search (this **is** Phase 14, not an addition to it)
- MCP server exposing the vault as a callable tool

**Explicitly out of scope for now:**
- Custom web UI (Obsidian is the UI until it demonstrably isn't enough)
- Mobile app, multi-user/team features
- Fine-tuning any model
- Building a note-taking app from scratch
- Audio transcription pipelines beyond what YouTube captions already provide

**MVP definition (what "done" looks like for Phase 0-1):** A git-initialized Obsidian vault with `raw/`, `wiki/`, and a schema file, containing at least 10 real ingested sources (a mix of your own project docs and 2-3 external articles/videos), browsable via Obsidian's graph view, with wiki pages that were agent-generated, not hand-typed.

---

## 5. Assumptions and Constraints

Labeled assumptions — flag any of these that are wrong and the plan adjusts:

- **A1:** You're proceeding with Docker (already a working skill) and continued Groq API access (already integrated into 4+ of your projects).
- **A2 (resolved):** Provision for both. Groq API is the primary generation provider now (matches AlignResume/Overture/Future Fit). Ollama is uninstalled (8 GB RAM couldn't run a local LLM comfortably) but may return later on better hardware. Architecture decision: a thin provider-abstraction layer (§9.7) so swapping generation providers is a config change, not a rewrite. Embeddings are local from day one regardless (small models run fine on 8 GB RAM — see §9.7), which gets you "local by default" for search immediately without waiting on Ollama.
- **A3:** This slots into your **existing** 8–10 hrs/week technical study budget (DevOps + Agentic AI roadmaps combined) rather than adding new hours. Every phase below is written to displace or merge with weeks already allocated in those roadmaps, not sit alongside them.
- **A4:** You want both personal/project docs and external articles/videos in the same vault (explicitly stated) — not two separate systems.
- **Constraint:** Must not duplicate the Phase 14 capstone effort. Where this plan's Phase 4 and your Mission Plan's DevOps Phase 14 overlap, they are treated as the same work, per your own "one checkpoint satisfies both roadmaps" principle (Section 9 of the Mission Plan).
- **Open/unconstrained:** OS not specified — every tool recommended below (Obsidian, Python, Docker, Git) is cross-platform, so this isn't blocking.

---

## 6. Stakeholders / Users

| Role | Who |
|---|---|
| Primary user | You |
| Approver / QA | You (solo project — no external review gate) |
| Downstream consumer #1 | Future Conductor (queries "what do I already know about X" mid-orchestration) |
| Downstream consumer #2 | Memory Module (Agent #8) — reuses this exact infrastructure |
| Downstream consumer #3 | Future-you at the FDE phase, recalling specific enterprise-integration patterns learned years earlier |

---

## 7. Success Criteria

| Metric | Target | How measured |
|---|---|---|
| Ingestion latency | New source → wiki page within 48h | Check `log.md` timestamps |
| Vault growth | 20+ sources ingested within 30 days of Phase 0 | Count `wiki/sources/` entries |
| Link density | Every wiki page has ≥2 cross-references after Month 1 | `lint` agent output |
| Automation | Zero manual copy-paste into an LLM chat by end of Phase 3 | Ingest agent runs unattended via scheduler |
| Retrieval quality | RAGAS faithfulness/relevance scores above your own defined threshold | Phase 4 eval suite (same rubric as Phase 14 capstone) |
| MCP exposure | An external MCP client can query the vault and get a cited answer | Phase 5 acceptance test |
| Orphan rate | 0 broken wikilinks after monthly `lint` | `lint` agent report |

---

## 8. Project Breakdown (Modules)

| Module | Purpose | Inputs | Outputs | Dependencies | Priority | Order |
|---|---|---|---|---|---|---|
| **M1 — Capture Layer** | Get raw material into `raw/` with zero friction | URLs, YouTube links, local files, dropped-in personal docs, **existing notes scattered across Android, computer folders, and Google Drive** | Cleaned text files in `raw/sources/` | None | Must-have | 1 |
| **M2 — Storage Layer** | Durable, versioned, queryable substrate | `raw/` content | Git-versioned vault; optional SQLite metadata table (`sources`, `tags`, `pages`) | M1 | Must-have | 2 |
| **M3 — Agent Layer** | Ingest, link, lint, digest — the "AI maintains it" requirement | New raw sources + existing wiki state | Updated `wiki/*.md`, `index.md`, `log.md` | M2, an LLM API | Must-have | 3 |
| **M4 — Search-at-Scale Layer** | Semantic query once vault outgrows manual browsing | `wiki/` pages (curated, not raw dumps) | Qdrant collection (embedded via a local `sentence-transformers` model, not Groq) + RAGAS eval report | M3, Docker (already known) | Should-have (becomes must-have past ~150 pages) | 4 |
| **M5 — Interface Layer** | How you and other tools read/write the vault | Obsidian (primary); optional CLI; optional MCP server | Browsable graph, query responses | M2–M4 | Should-have | 5 |
| **M6 — Integration Layer** | Connects to the rest of your architecture | MCP server from M5 | Conductor can call the vault; Memory Module reuses the schema | M5 | Nice-to-have (near-term), Must-have (long-term) | 6 |

---

## 9. Architecture / Structure

### 9.1 Folder structure

```
second-brain/
├── raw/                      # Immutable source of truth — agent reads, never edits
│   ├── sources/              # Clipped articles, video transcripts, dropped docs
│   └── assets/               # Images, PDFs, attachments
├── wiki/                     # AI-maintained layer — you read it, the agent writes it
│   ├── sources/              # One summary page per ingested source
│   ├── entities/             # People, companies, tools (e.g., "Qdrant", "IIT Roorkee", "Groq")
│   ├── concepts/              # Ideas/frameworks (e.g., "RAG vs Wiki-pattern", "GLMM")
│   ├── projects/              # YOUR OWN project pages — AlignResume, Gleaner, Conductor, etc.
│   ├── synthesis/             # Cross-source comparisons, weekly digests
│   ├── index.md               # Master catalog — all pages, all links
│   └── log.md                 # Chronological record of every ingest/link/lint/digest run
├── output/                    # Generated reports (e.g., weekly digest exports)
├── db/                        # SQLite metadata (sources, tags, embeddings_ref) — optional, Phase 2+
├── SCHEMA.md                  # The conventions file — page types, tagging rules, workflows
└── .git/                      # Version history, private remote for backup
```

### 9.2 Data flow

```
[Article URL] ──┐
[YouTube link] ──┼──► Capture scripts ──► raw/sources/*.md (cleaned text + metadata)
[Local file]  ──┘                              │
[Your own project docs] ─────────────────────►┘
                                                │
                                    ┌───────────▼────────────┐
                                    │   INGEST AGENT          │
                                    │  reads raw/, checks     │
                                    │  wiki/index.md, decides │
                                    │  what pages to create/  │
                                    │  update                 │
                                    └───────────┬────────────┘
                                                │
                        ┌───────────────────────┼───────────────────────┐
                        ▼                       ▼                       ▼
                 wiki/sources/*.md       wiki/entities/*.md      wiki/concepts/*.md
                        │                       │                       │
                        └───────────┬───────────┴───────────────────────┘
                                    ▼
                            LINK AGENT (cross-references)
                                    ▼
                            LINT AGENT (weekly — broken links, dupes)
                                    ▼
                            DIGEST AGENT (weekly — wiki/synthesis/YYYY-Www.md)
                                    │
                        (past ~150 pages, add:)
                                    ▼
                    Qdrant embeds wiki/*.md → semantic search → RAGAS eval
                                    │
                                    ▼
                        MCP server exposes: search_second_brain,
                        get_entity_page, ingest_source
                                    │
                                    ▼
                    Conductor / any MCP client can query your own knowledge
```

### 9.3 Design principle: wiki-first, vector-search-second

The Karpathy pattern's core bet is that a curated wiki page — written once, updated incrementally — answers most questions better than re-retrieving raw chunks every time. Standard RAG chunks documents and searches at query time; that works but degrades as the corpus grows and questions get more conceptual. This plan treats vector search (M4/Qdrant) as an **index over the wiki**, not a replacement for it — you embed the clean `wiki/` pages, not the messy `raw/` dumps. That also makes the Qdrant/RAGAS layer smaller and higher-signal than a typical from-scratch RAG project, which is a genuine improvement worth noting in whatever writeup you produce for the Phase 14 capstone.

### 9.4 Content sensitivity tiering

Some of what will go into `raw/` is career/technical material meant to be cited and reused freely. Some of it — planning documents, personal reflection — is not something you'd want summarized by a third-party API without thinking about it first. Before ingesting anything personal, split `raw/sources/` into a `public/` and `private/` sub-tier at the schema level, and decide per-tier whether cloud API calls (Groq/Claude) are acceptable or whether that tier should route through a local model instead (see Open Questions, Q1). This is a five-minute decision now that avoids a much more annoying migration later.

### 9.5 Schema file (starting template)

```markdown
# SCHEMA.md — Second Brain Conventions

## Page types
- source: one per ingested raw item (article/video/doc). Frontmatter: source_url, 
  type [article|video|doc|project], date_ingested, one-line "why I saved this"
- entity: person, org, tool, product
- concept: idea, framework, technique
- project: YOUR projects specifically (AlignResume, Gleaner, Conductor, Overture, 
  Future Fit, Veritas, Altitude & Heat) — status field synced from Mission Plan
- synthesis: weekly digest, cross-source comparison

## Ingest workflow
1. Read new files in raw/sources/ not yet in log.md
2. For each: write/update a `source` page, extract entities/concepts, 
   create or link to their pages
3. Append entry to log.md
4. Update index.md

## Lint workflow (weekly)
- Find broken [[wikilinks]]
- Flag pages with no incoming or outgoing links (orphans)
- Flag near-duplicate source pages

## Digest workflow (weekly)
- Summarize the week's log.md entries into wiki/synthesis/YYYY-Www.md
- Surface any contradictions or repeated themes across sources
```

### 9.6 Buy vs. build — agent runtime — two separate decisions

v1.1 treated this as one decision. It's actually two, and conflating them was the mistake — corrected here.

**Decision A — what executes continuously (the runtime agent stack):**

| Option | Learning value toward Stage 03 | Reuses existing stack | Status |
|---|---|---|---|
| Claude Code (or similar) driving the ingest/link/lint loop directly, continuously, in production | Low — you're operating a tool, not building the agent loop | No | Not selected as runtime |
| **Hand-rolled Python + Groq API + cron** | High — "write the loop by hand before the framework," your own Stage 03 principle | Yes — same Groq API already in 4 projects | **Selected — unchanged from v1.1** |
| LangGraph orchestration of the same agents | High — direct Stage 03 checkpoint | Yes | Adopted once the hand-rolled loop works (Phase 3) |

**Decision B — what helps you write that Python code (development tooling):**

| Tool | Role | Status |
|---|---|---|
| Claude Code | AI-assisted scaffolding/pair-programming while you architect | **In provision** |
| Antigravity | Same role — already used on AlignResume | **In provision** |
| Codex | Same role — already used on AlignResume | **In provision** |
| Manual, unassisted | Fallback for anything you specifically want to hand-type | Available, not required |

Why the split holds up: this mirrors the same distinction your Job Prep doc already draws for AlignResume — architecture-level rigor and personal-skill-level claims are two different things, and AI-assisted construction is legitimate as long as you can independently explain every decision afterward. Claude Code/Antigravity/Codex can write the capture scripts, the provider abstraction, the ingest/link/lint/digest logic, and the MCP server. What still satisfies Stage 03's actual requirement ("the loop hand-built before the framework") is that the *architecture* is yours — you're directing what the loop does and why, at the level this document specifies — not that you personally typed every line. What runs continuously once built is still pure Python + Groq calls on a schedule, not an agent-framework abstraction and not a coding assistant maintaining the wiki in production.

Practically: use Claude Code/Antigravity/Codex from Phase 1 onward to build each script in §10 faster. Phase 0's manual copy-paste bridge stays as-is for the first 5 pages — that step is about getting content into the vault before any code exists, unrelated to this decision.

### 9.7 Inference Provider Abstraction

Two providers, one interface, so switching is a one-line config change rather than a rewrite:

```python
# providers/base.py
from abc import ABC, abstractmethod

class GenerationProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str: ...

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...
```

```python
# providers/groq_provider.py — generation, active now
class GroqProvider(GenerationProvider):
    def generate(self, prompt: str) -> str:
        # existing Groq client pattern from Overture/AlignResume
        ...
```

```python
# providers/ollama_provider.py — generation, dormant until reinstalled
class OllamaProvider(GenerationProvider):
    def generate(self, prompt: str) -> str:
        # same interface; only this file changes when Ollama comes back
        ...
```

```python
# providers/local_embeddings.py — active from day one, independent of the above
from sentence_transformers import SentenceTransformer

class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        # ~80MB, CPU-only, comfortable on 8GB RAM — this is not the part
        # that struggled with Ollama; generation (a full LLM) was.
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()
```

`SCHEMA.md` or a `config.yaml` picks the active generation provider by name; `LocalEmbeddingProvider` is not swapped — it's the permanent default, since it's what makes M4 (search-at-scale) genuinely local regardless of what the RAM situation is on any given day. This resolves the "provision for both" requirement cleanly: embeddings are always local, generation is Groq today and Ollama whenever the hardware allows it, and the agent code in Phase 3 never needs to know which one is active.

Note on Groq specifically: Groq's confirmed strength across your existing projects is chat completion (and speech-to-text). Whether Groq's API currently exposes a dedicated embeddings endpoint is genuinely unclear from available documentation — recommendations are mixed. Rather than depend on that being available, this design sidesteps the question entirely by keeping embeddings local. Worth a quick check of console.groq.com/docs if you want certainty, but it doesn't block anything here.

---

## 10. Execution Roadmap

| Phase | Timeframe | Objective | Key Deliverables | Maps to Existing Roadmap |
|---|---|---|---|---|
| **0 — Seed the Vault** | Days 1–3 | Start capturing today, zero engineering | Git-init'd Obsidian vault; `raw/`, `wiki/`, `SCHEMA.md`; 5 real sources dropped in (mix of your own docs + 1–2 articles); first wiki pages generated (manual LLM copy-paste is fine here) | New — pure bootstrap |
| **0.5 — Legacy Consolidation** | Days 4–7 | One-time pull of everything already scattered across Android, computer folders, and Google Drive into `raw/sources/` before building new habits on top of an incomplete base | `drive_import.py` using Google Drive API (reuse the OAuth2 flow already built for Overture Outreach's Gmail integration — same auth pattern, different scope); manual export/copy for anything trapped in an Android-only note app with no sync; everything landing in `raw/sources/` with a `source: legacy-import` tag so it's distinguishable from new captures | New — but the OAuth2 mechanics are a direct reuse of Overture Outreach, not new learning |
| **1 — Habit + Schema Lock-in** | Week 1–2 | Formalize page types; add the manual "why I saved this" annotation step; ingest your own Mission Plan/Skills Profile/Job Prep docs as the first `project` and `entity` pages | Stable `SCHEMA.md`; 10–15 sources ingested (now including the legacy import backlog); first real payoff — your own docs are now wiki pages | Runs alongside DevOps roadmap Phase 1–2 (Linux/networking weeks) |
| **2 — Multi-Source Capture Automation** | Week 3–5 | Script the URL/video/local-file capture so it's not copy-paste | `capture_article.py` (trafilatura-based), `capture_youtube.py` (youtube-transcript-api), `capture_watch.py` (watchdog on an inbox folder) | Reinforces Python/Pandas applied-refresher goal (real project, not tutorials) |
| **3 — Agent Maintenance Loop** | Week 6–8 | Replace manual LLM copy-paste with an unattended ingest/link/lint/digest agent | Hand-rolled Python agent loop calling Groq API; scheduled via cron/Task Scheduler; `log.md` and `index.md` updating themselves | Direct Stage 03 checkpoint: "the agent loop, hand-written before the framework" |
| **4 — Search-at-Scale (Qdrant + RAGAS)** | Week 9–11 | Semantic search once the vault is large enough that browsing alone isn't enough | Qdrant container; wiki pages embedded (not raw dumps); RAGAS eval suite; tracing | **This IS DevOps roadmap Phase 14** — same checkpoint, no separate time budget needed |
| **5 — MCP Exposure + Conductor Integration** | Week 12–14 | Make the vault queryable by any MCP client | MCP server: `search_second_brain`, `get_entity_page`, `ingest_source`; Conductor wired to call it | Direct Stage 03 checkpoint: "build a custom MCP server exposing a callable tool"; prototype for Memory Module (#8) |
| **6 — Hardening & Standing Ops** | Ongoing | Keep it alive without babysitting it | pytest coverage on capture/parsing functions; Docker Compose for the full stack; weekly digest + monthly lint as calendar-scheduled habits; README + ADRs | Matches your existing engineering principles (testing, documentation-first) |

---

## 11. Risks and Mitigations

| Risk | Probability | Impact | Mitigation | Fallback |
|---|---|---|---|---|
| Automation stops running and nobody notices | Medium | High (wiki value decays silently) | Scheduled job + a log-based tripwire: if `log.md` hasn't been touched in 14 days, surface a warning next time you open the vault | Manual weekly digest run as a backup habit |
| Passive hoarding — clipping without engaging | Medium | Medium (defeats the point) | Mandatory one-line "why I saved this" before any source gets ingested (Phase 1 schema rule) | Periodic manual review of `raw/` for anything never annotated |
| Schema over-engineered before content exists | Medium | Medium (delays Phase 0) | Seed with 5–10 real sources first; let page types emerge; don't design the full ontology upfront | Revisit `SCHEMA.md` after Week 2, not before |
| Scope creep — building a custom UI too early | Medium | Medium (time sink, no functional gain yet) | Obsidian is the UI through Phase 4 minimum; custom UI only if Obsidian's search genuinely becomes insufficient | None needed — this is a hard rule, not a preference |
| Duplicated effort with existing Phase 14 plan | Low (now that it's explicitly merged) | High if unmerged | Treat Phase 4 of this plan and Mission Plan Phase 14 as one deliverable | N/A — this document is the fix |
| Single-machine fragility | Low | High (data loss) | Private git remote (GitHub, already your daily tool) as backup | Local Time Machine/File History as a second layer |
| Sensitive personal content processed by cloud APIs without thinking about it | Medium | Medium–High depending on content | `public/` vs `private/` tiering in `raw/`, decided before first ingest of anything personal (see §9.4) | Route `private/` tier through a local model if needed (Ollama, once reinstalled) |
| Legacy note formats fragment the import (Google Keep vs. Samsung Notes vs. plain files export very differently) | Medium | Medium (Phase 0.5 stalls) | Drive-synced content goes through the Drive API path; anything else gets manually exported once as a batch, tagged `legacy-import`, and never revisited as a recurring process | Treat Phase 0.5 as a one-time cost, not a maintained pipeline |
| Local embedding model too heavy for the 8GB machine | Low | Medium (M4 blocked) | `all-MiniLM-L6-v2` (~80MB) or similarly small sentence-transformers model — this is not the class of model that struggled with Ollama; full generative LLMs and small embedding models have very different RAM footprints | Drop to an even smaller model (e.g., a 20–30M parameter variant) if needed |
| AI-assisted-written code (Claude Code/Antigravity/Codex) isn't fully internalized before an interview | Medium | Medium — same risk already flagged for AlignResume in the Job Prep doc | You architect and direct every module in §8/§10; the tools implement. Before marking any phase "done," do a self-walkthrough of that phase's code out loud, as if explaining it live, with no notes | Re-read the module with the tool present and have it quiz you on the architectural decisions |

---

## 12. Prioritized Next Actions

Do these in the next 7 days, in order — this mirrors the exact "three questions, no code" unlock you already used successfully for Conductor:

1. **Write `SCHEMA.md`** — three answers, no code: (a) what counts as a page type, (b) what happens on ingest in what order, (c) what a query returns at the end. Use §9.5 above as the starting draft.
2. **Create the vault** — Obsidian, `git init`, the five folders from §9.1. Fifteen minutes.
3. **Drop in 5 real sources** — at minimum: your Mission Plan PDF (as the first `project` pages), one article you've actually read recently, one video you've actually watched recently.
4. **Generate the first wiki pages manually** — paste the schema + sources into a Claude/Groq chat session, ask it to produce the `source` and `project` pages per the schema. This is Phase 0's entire scope. Do not start scripting yet.
5. **Decide the sensitivity tiering question (§9.4) before ingesting anything personal.**
6. **Identify what actually holds your existing Android notes** (Google Keep, Samsung Notes, plain files, or something else) — this determines whether Phase 0.5's Drive API pull covers everything or needs a manual export step alongside it.

---

## 13. Long-Term Strategy

Past Phase 6, three natural extensions, in likely order of value:

1. **Fold it into Conductor formally.** Once M6 (MCP exposure) exists, Conductor's Research Agent can query "what do I already know about this company/topic" before doing fresh research — closing a loop your AI Job Agent Architecture already anticipates via the shared Candidate Profile JSON pattern.
2. **Let it absorb the "Living Notes" maintenance job.** Your Part I §13 update log ("what to update next" checklist) is exactly the kind of small, recurring documentation chore this system is built to automate. Once Phase 3's agent loop is stable, point it at your own Mission Plan/Skills Profile/Job Prep docs as living `project` pages instead of manually-versioned PDFs.
3. **Consider the productization angle, later, not now.** Section 12 of your Mission Plan already lists "small digital products built on the agent architecture already in development" as a Phase 3+ income stream. A working personal-knowledge-agent is directly adjacent to your stated Phase 5 business category (AI Automation/Agentic Orchestration). Flagging this now only so it's not invented later — no action needed until the underlying system is actually stable and used daily for a few months.

---

## 14. Open Questions

~~1. Fully local vs. cloud inference~~ — **Resolved:** provision for both, via the provider abstraction in §9.7. Groq now, Ollama later, embeddings always local.
~~2. Existing notes elsewhere~~ — **Resolved:** Android, computer folders, and Google Drive. Folded into Phase 0.5.
~~3. Claude Code vs. pure Python~~ — **Resolved:** pure Python, from Phase 0 onward (§9.6).

New questions surfaced by those answers:

1. **Which app actually holds the Android notes?** Google Keep and most other Android note apps sync to Google Drive, which the Phase 0.5 Drive API pull already covers. Samsung Notes and a few others don't sync anywhere by default and would need a one-time manual export. Worth checking before Day 4.
2. **Roughly how many existing notes/files are we talking about?** A few dozen vs. several hundred changes whether Phase 0.5 is a half-day task or needs its own batching/rate-limit handling in `drive_import.py`.

---

*End of plan. Treat this file itself as the first `project` page ingested into the vault once Phase 0 is live.*
