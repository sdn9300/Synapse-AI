# SYSTEM EVALUATION PLAN & QUALITY BENCHMARKS — SECONDSELF

**Document Version:** 1.0  
**Status:** Approved Quality & Evaluation Specification  
**System Name:** SecondSelf Personal AI Second Brain  
**Evaluation Framework:** RAGAS Evaluation Metrics + Vault Health Metrics + End-to-End Pipeline Benchmarks

---

## 1. Executive Summary & Evaluation Objectives

The objective of the **SecondSelf Evaluation Plan** is to provide rigorous, measurable, and automated quality assurance across all layers of the Personal AI Second Brain. 

Unlike standard search systems evaluated on synthetic datasets, SecondSelf is evaluated against **real personal knowledge data** (project documentation, research notes, saved bookmarks, and technical PDFs). Evaluation covers three distinct dimensions:

1. **RAG Retrieval & Generation Quality (RAGAS Framework):** Measuring answer accuracy, relevance, and grounding.
2. **Vault Topology & Link Density:** Measuring graph connectivity, categorization accuracy, and orphan rate.
3. **Operational Performance & Latency:** Measuring capture latency, classification speed, and UI responsiveness.

---

## 2. Quantitative Metric Rubric

| Category | Metric Name | Target Threshold | Measurement Method | Evaluation Frequency |
|---|---|---|---|---|
| **RAG** | **Faithfulness** | $\ge 0.85$ | RAGAS / LLM-as-a-Judge verify statement grounding | Weekly |
| **RAG** | **Answer Relevance** | $\ge 0.80$ | Cosine similarity between query and generated answer | Weekly |
| **RAG** | **Context Recall** | $\ge 0.75$ | Check if ground-truth facts exist in top-$K$ notes | Bi-weekly |
| **RAG** | **Context Precision** | $\ge 0.80$ | Ratio of relevant retrieved notes to total top-$K$ | Bi-weekly |
| **Vault** | **Categorization Accuracy** | $\ge 90\%$ | Manual spot-check of PARA assignment | Monthly |
| **Vault** | **Link Density** | $\ge 2.0$ links/note | Total edges / Total notes in `data/graph.json` | Weekly |
| **Vault** | **Orphan Rate** | $0\%$ broken links | `lint` script check for unlinked/broken `[[wikilinks]]` | Monthly |
| **Perf** | **Capture Latency** | $< 2.0$ seconds | Execution time of `capture.py` CLI command | Per commit |
| **Perf** | **Pipeline Latency** | $< 30$ seconds | Total time to classify & link 10 items | Per release |
| **Perf** | **UI Load Time** | $< 1.5$ seconds | Browser load time for Streamlit app & Graph HTML | Per release |

---

## 3. RAGAS Evaluation Framework Specification

SecondSelf adopts the **RAGAS (Retrieval-Augmented Generation Assessment System)** framework to evaluate retrieval quality and LLM synthesis.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   USER QUERY STRING                                    │
└───────────────────────────┬────────────────────────────────────────────┘
                            │
                     ┌──────┴──────────────────────┐
                     ▼                             ▼
┌──────────────────────────────────────────┐     ┌───────────────────────────────────────┐
│         RETRIEVED CONTEXT (Top-K)        │     │           GENERATED ANSWER            │
└────────────────────┬─────────────────────┘     └─────────────────┬─────────────────────┘
                     │                                             │
                     ├──────────────────────┬──────────────────────┤
                     ▼                      ▼                      ▼
┌──────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────────┐
│       FAITHFULNESS       │   │     ANSWER RELEVANCE     │   │    CONTEXT PRECISION     │
│ Are answer statements    │   │ Does answer directly     │   │ Are top ranked notes     │
│ supported by context?    │   │ address user question?   │   │ high signal / relevant?  │
└──────────────────────────┘   └──────────────────────────┘   └──────────────────────────┘
```

### 3.1 Faithfulness Score Calculation
* **Definition:** Measures the proportion of claims in the generated answer that can be directly inferred from the retrieved note contexts.
* **Formula:**
  $$\text{Faithfulness} = \frac{\text{Number of claims in answer supported by context}}{\text{Total number of claims in answer}}$$
* **Guardrail Target:** $\ge 0.85$. Answers containing unsupported hallucinations are flagged as failures.

### 3.2 Answer Relevance Score Calculation
* **Definition:** Measures how pertinent the generated answer is to the user's query.
* **Method:** Compute cosine similarity between the embedding of the question $V(Q)$ and the embedding of generated answer $V(A)$:
  $$\text{Relevance} = \cos(V(Q), V(A)) = \frac{V(Q) \cdot V(A)}{\|V(Q)\| \|V(A)\|}$$
* **Guardrail Target:** $\ge 0.80$. Answers that wander off-topic are penalized.

### 3.3 Context Recall & Precision
* **Context Recall:** Evaluates whether all key facts needed to answer the question were retrieved in top-$K$ notes.
* **Context Precision:** Evaluates whether relevant notes are ranked higher than noise notes in the retrieval list.

---

## 4. Vault Topology & Health Evaluation

### 4.1 Link Density & Graph Connectivity Benchmark
* **Objective:** Ensure knowledge compounds over time through cross-referencing rather than remaining isolated islands.
* **Calculation:**
  $$\text{Link Density} = \frac{2 \times |E|}{|V|}$$
  where $|E|$ is the total number of edges in `data/graph.json` and $|V|$ is the total number of nodes.
* **Target:** Minimum $2.0$ links per note after 30 days of active vault ingestion.

### 4.2 Orphan Rate & Broken Wikilink Audit
* **Broken Wikilinks:** Any `[[target-id]]` string in a note body where `target-id` does not exist in `wiki/**/*.md`.
* **Orphan Notes:** Nodes in `data/graph.json` with degree $= 0$ (no incoming or outgoing edges).
* **Target:** $0$ broken wikilinks and $< 5\%$ orphan notes after monthly linting.

---

## 5. Automated Evaluation Script Specification (`eval_benchmark.py`)

Below is the design specification for an automated evaluation benchmark script:

```python
"""
Automated Evaluation Benchmark Suite for SecondSelf (EVALUATION_PLAN.md).
Evaluates retrieval accuracy, cosine similarity relevance, and vault link density.
"""

import json
from pathlib import Path
from lib.storage import read_wiki_notes, GRAPH_FILE
from lib.embeddings import embed_text, cosine_similarity
from ask import ask


def run_evaluation_suite():
    print("=== RUNNING SECONDSELF EVALUATION BENCHMARK SUITE ===")
    
    # 1. Vault Health Audit
    notes = read_wiki_notes()
    total_notes = len(notes)
    note_ids = {n.id for n in notes}
    
    broken_links = 0
    total_links = 0
    for note in notes:
        for link in note.links:
            total_links += 1
            if link not in note_ids:
                broken_links += 1
                
    orphan_notes = [n.id for n in notes if not note.links]
    
    print(f"\n1. VAULT TOPOLOGY METRICS:")
    print(f" - Total Wiki Notes: {total_notes}")
    print(f" - Total Cross-Links: {total_links}")
    print(f" - Broken Wikilinks: {broken_links}")
    print(f" - Orphan Notes: {len(orphan_notes)} ({len(orphan_notes)/max(1, total_notes)*100:.1f}%)")
    
    # 2. Graph Metadata Audit
    if GRAPH_FILE.exists():
        with open(GRAPH_FILE, "r", encoding="utf-8") as f:
            gdata = json.load(f)
            node_cnt = gdata.get("metadata", {}).get("node_count", 0)
            edge_cnt = gdata.get("metadata", {}).get("edge_count", 0)
            density = (2 * edge_cnt) / max(1, node_cnt)
            print(f" - Graph Nodes: {node_cnt} | Edges: {edge_cnt} | Density: {density:.2f}")

    # 3. RAG Relevance Test
    test_queries = [
        "What are the core goals of SecondSelf?",
        "Explain the DevOps Phase 14 capstone requirements",
        "What local embedding model is used for auto-linking?",
    ]
    
    print(f"\n2. RAG RETRIEVAL & RELEVANCE METRICS:")
    for q in test_queries:
        res = ask(q, top_k=3)
        q_vec = embed_text(q)
        a_vec = embed_text(res.answer)
        rel_score = cosine_similarity(q_vec, a_vec)
        print(f" - Query: '{q}'")
        print(f"   Relevance: {rel_score:.3f} | Top Source: {res.sources[0]['id'] if res.sources else 'None'}")

    print("\n=== EVALUATION BENCHMARK COMPLETED ===")

if __name__ == "__main__":
    run_evaluation_suite()
```
