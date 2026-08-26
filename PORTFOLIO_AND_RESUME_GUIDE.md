# 📄 Synapse-AI — Portfolio, Resume & Career Guide

This guide provides high-impact, professional copy for your **Resume**, **Portfolio Website**, **LinkedIn**, and **Technical Interview Talking Points** for **Synapse-AI**.

---

## 📄 1. Resume Bullet Points

### Option A: Standard Resume Bullets (High Impact / Action-Oriented)
> **Synapse-AI — Personal AI Second Brain & Graph-RAG System** | *Python, Groq API, Streamlit, SentenceTransformers, Vis-Network, MCP* | [GitHub Link](https://github.com/sdn9300/Synapse-AI)
> * Architected and deployed an autonomous, local-first Personal Knowledge Management (PKM) system leveraging the **Karpathy LLM Wiki pattern** and **PARA framework** for dynamic note organization and retrieval.
> * Built a multi-source ingest pipeline handling plain text, web URLs, Obsidian inbox notes, and local PDFs with **SHA-256 deduplication** and automated LLM categorization via **Groq Llama 3.3 70B & 3.1 8B**.
> * Engineered an automated vector auto-linker using **384-dimensional local dense embeddings** (`all-MiniLM-L6-v2`) and Cosine Similarity ($\ge 0.75$) to construct dynamic `[[wikilinks]]` cross-references.
> * Implemented an interactive force-directed knowledge graph UI using **Vis-Network** with Barnes-Hut physics and real-time node hover inspection.
> * Developed a **Retrieval-Augmented Generation (RAG)** Q&A engine and **Model Context Protocol (MCP) Tool Server**, exposing custom tools (`search_second_brain`, `get_wiki_page`, `ingest_raw_content`) for external AI agent orchestration.
> * Engineered vault health and maintenance automation, including `lint.py` for broken link/orphan note detection, `digest.py` for weekly executive LLM summaries, and an automated 12-test unit test suite (`test_secondself.py`).

### Option B: Concise / One-Liner (For Compact Resumes)
> **Synapse-AI** — Architected a local-first Personal AI Second Brain & Graph-RAG system using Python, Groq (Llama 3.3), local vector embeddings, Streamlit, and Vis-Network; features automated PARA classification, `[[wikilink]]` graph auto-linking, automated vault linting/digests, and a custom Model Context Protocol (MCP) tool server.

---

## 🌐 2. Portfolio Website & Project Showcase

### **Synapse-AI — Autonomous Personal Knowledge Brain & Graph-RAG Engine**

#### **Project Overview**
Synapse-AI is an end-to-end, local-first **Personal AI Second Brain** built on the **Karpathy LLM Wiki pattern**. It solves the core problem of digital information decay by automatically classifying, linking, visualizing, and answering natural language queries over accumulated notes, articles, research papers, and code documentation.

#### **Key Technical Highlights**
* **Multi-Source Autonomous Ingestion Pipeline:** Accepts plain text notes, web URLs, Obsidian inbox staging entries, and technical PDF files, extracting and normalizing content using BeautifulSoup4 and PyPDF with strict SHA-256 content deduplication.
* **PARA Framework AI Classification:** Automatically categorizes incoming captures into *Projects*, *Areas*, *Resources*, or *Archives* with YAML frontmatter metadata using Groq Llama 3.3 70B & 3.1 8B (with intelligent rule-based fallback).
* **Local Vector Auto-Linking:** Computes 384-dimensional embeddings on host hardware using `sentence-transformers/all-MiniLM-L6-v2` to evaluate cosine similarity matrix ($\ge 0.75$) and automatically establish bidirectional `[[wikilinks]]`.
* **Interactive Force-Directed Knowledge Graph:** Renders topological knowledge clusters in an HTML5 `vis-network` canvas configured with Barnes-Hut physics, group color-coding, and hover tooltips.
* **Grounded RAG Search Engine:** Natural language Q&A engine synthesizing answers strictly from top-$K$ retrieved note contexts with inline source citations (`[note-id]`).
* **Model Context Protocol (MCP) Integration:** Exposes an MCP Tool Server allowing multi-agent orchestrators to query personal knowledge, retrieve wiki notes, and push new captures asynchronously.
* **Vault Health & Weekly Synthesis Agents:** Includes an automated `lint.py` audit agent for broken link/orphan note detection and `digest.py` for weekly executive LLM synthesis reports.
* **Obsidian Vault & Staging Inbox:** Features native bidirectional workflow support for Obsidian vaults with automated inbox staging.

#### **Tech Stack**
`Python 3.10+` • `Groq API (Llama 3.3 / 3.1)` • `SentenceTransformers` • `Streamlit` • `Vis-Network (HTML5/JS)` • `Model Context Protocol (MCP)` • `NumPy` • `PyPDF` • `BeautifulSoup4` • `PyYAML`

---

## 💼 3. LinkedIn Announcement / Post Copy

> 🚀 **Excited to share my latest project: Synapse-AI!**
>
> Traditional note apps often become digital graveyards where captured bookmarks and research vanish without compounding value. 
> 
> To solve this, I built **Synapse-AI** — an autonomous, local-first **Personal AI Second Brain** and **LLM Wiki** inspired by Andrej Karpathy's LLM Wiki pattern.
> 
> 🧠 **What it does:**
> 1. **Multi-Source Ingestion:** Ingests notes, web URLs, Obsidian inbox entries, and PDFs with SHA-256 deduplication.
> 2. **AI Classification:** Auto-files content using the PARA framework (*Projects, Areas, Resources, Archives*) powered by Groq Llama 3.3 & 3.1.
> 3. **Local Vector Auto-Linking:** Computes 384-dim embeddings (`all-MiniLM-L6-v2`) to auto-insert `[[wikilinks]]` between related notes.
> 4. **Interactive Graph UI:** Visualizes knowledge topology using a force-directed `vis-network` physics canvas.
> 5. **Grounded RAG Q&A:** Synthesizes natural-language answers with inline source citations.
> 6. **MCP Tool Server:** Exposes custom Model Context Protocol tools for external AI agent integration.
> 7. **Obsidian Vault Integration:** Direct support for staging notes in Obsidian and automated inbox ingestion.
> 
> 🛠️ **Tech Stack:** Python, Groq API, SentenceTransformers, Streamlit, Vis-Network, MCP, NumPy.
> 
> 🔗 Check out the open-source GitHub repository here: https://github.com/sdn9300/Synapse-AI
> 
> #AI #MachineLearning #RAG #GraphRAG #Python #OpenSource #SoftwareEngineering #MCP #SecondBrain #Obsidian

---

## 🗣️ 4. Technical Interview Talking Points ("Tell me about a complex system you built")

### **The Problem:**
*"Every note-taking app fails because knowledge capture is un-maintained and knowledge decays over time. Notes sit in folders nobody re-reads, and bookmarks pile up without compounding value."*

### **The Solution & Architecture:**
*"I built Synapse-AI, a local-first AI Second Brain based on the Karpathy LLM Wiki pattern. It uses an autonomous 4-stage agent loop: Ingest $\rightarrow$ Link $\rightarrow$ Lint $\rightarrow$ Digest. When content lands in `raw/` or `wiki/Inbox/`, it extracts text from HTML or PDFs, runs PARA classification using Groq Llama 3, computes 384-dimensional embeddings using `sentence-transformers` locally on host CPU, and auto-inserts cross-references (`[[wikilinks]]`) when cosine similarity exceeds 0.75."*

### **Key Technical Challenges & Design Choices:**
1. **Wiki-First vs. Vector-Second:** *"Instead of chunking raw noisy dumps at search time, the AI maintenance loop creates clean, curated Markdown wiki pages first. Vector embeddings are computed over clean notes, resulting in significantly higher signal-to-noise ratio during RAG retrieval."*
2. **Defensive Fallback & Reliability:** *"I engineered active model failover for Groq APIs (Llama 3.3 70B, Llama 3.1 8B) and rule-based heuristic fallbacks for classification and vector math so the pipeline runs reliably even if API rate limits or network dropouts occur."*
3. **Agent Integration via MCP:** *"I exposed the system as an MCP (Model Context Protocol) tool server, allowing external agent orchestrators to query personal knowledge as a native tool call."*
