# CORNER SCENARIOS & EDGE-CASE PLAN — SECONDSELF

**Document Version:** 1.0  
**Status:** Approved Edge Case Specification  
**System Name:** SecondSelf Personal AI Second Brain  
**Scope:** Full-Stack Defensive Handling (Capture, Scraping, LLM, Vector Math, Graph Rendering, Data Concurrency)

---

## 1. Executive Overview & Defensive Principles

A robust personal knowledge system must handle unexpected user inputs, network failures, malformed LLM outputs, and edge cases gracefully without crashing or corrupting data.

SecondSelf adopts four core defensive engineering principles:

1. **Fail-Safe Fallbacks:** Never allow an external API failure (e.g., Groq rate limits, web scraping timeouts) to crash the application. Fallback to heuristic classification, local metadata extraction, or deterministic vector math.
2. **Data Immutability Guard:** Raw captures (`raw/`) land as immutable records. Even if classification or linking fails, raw content is preserved and can be re-processed anytime.
3. **Idempotent Pipeline Processing:** Running `pipeline.py process` multiple times must produce identical, deduplicated results without creating duplicate wiki notes or repeated `[[wikilinks]]`.
4. **Graceful UI Degradation:** If graph data or embeddings are missing, the Streamlit interface displays helpful guidance messages rather than raising unhandled stack traces.

---

## 2. Comprehensive Edge Case Matrix

### 2.1 Category 1: Raw Capture & File IO Edge Cases

| ID | Edge Case Scenario | Risk Level | Expected System Behavior / Guardrail | Fallback Mechanism |
|---|---|---|---|---|
| **E1.1** | Local file path does not exist | Low | `capture_file()` detects missing file, prints error message, and exits with code 1. | Reject capture; prompt user for valid path. |
| **E1.2** | Empty note text or 0-byte file | Low | Reject capture with explicit warning: "Content cannot be empty." | Exit without writing `raw/` files. |
| **E1.3** | Duplicate content captured | Medium | `content_hash()` computes SHA-256 string. If hash matches existing capture, warn user of duplicate. | Allow capture but tag with metadata `duplicate_detected`. |
| **E1.4** | Extremely large file (>10MB) | Medium | Read file stream safely; cap text extraction at first 10,000 characters for LLM prompt. | Store full raw file; truncate text passed to classifier. |
| **E1.5** | Corrupt or password-protected PDF | Medium | `pypdf.PdfReader` fails during extraction. Wrap in `try-except`. | Fallback to extracting filename & file metadata string. |

---

### 2.2 Category 2: Web Scraping & Content Extraction Edge Cases

| ID | Edge Case Scenario | Risk Level | Expected System Behavior / Guardrail | Fallback Mechanism |
|---|---|---|---|---|
| **E2.1** | URL unreachable / 404 / 500 error | Medium | `requests.get()` throws HTTP error or connection timeout (set timeout = 5s). | Catch exception; classify raw URL string + optional user notes. |
| **E2.2** | Web page requires login / paywall | Medium | Scraper receives redirect or minimal text. | Extract `<title>` tag text; fallback to raw URL string. |
| **E2.3** | JavaScript-rendered Single Page App | Medium | Static HTML parsing via BeautifulSoup returns empty body. | Strip script tags; extract raw text meta tags + URL. |
| **E2.4** | HTML contains script/ad bloat | Low | Remove `<script>`, `<style>`, `<nav>`, `<header>`, `<footer>` elements before parsing text. | Clean whitespace and restrict body text to top 3000 chars. |

---

### 2.3 Category 3: LLM Inference & Classification Edge Cases

| ID | Edge Case Scenario | Risk Level | Expected System Behavior / Guardrail | Fallback Mechanism |
|---|---|---|---|---|
| **E3.1** | `GROQ_API_KEY` missing or invalid | Medium | `call_llm()` detects missing key, prints notice, skips HTTP request. | Fallback to rule-based heuristic PARA classifier (`classify_content()`). |
| **E3.2** | Groq API rate limit hit (HTTP 429) | High | Catch status code 429; log rate limit warning. | Fallback to heuristic classifier; preserve item for re-run. |
| **E3.3** | LLM output is malformed / non-JSON | High | RegEx regex `\{.*\}` fails to locate valid JSON structure in output. | Catch `JSONDecodeError`; trigger heuristic classifier fallback. |
| **E3.4** | LLM returns unknown PARA category | Low | Check if returned category $\in$ `['Projects', 'Areas', 'Resources', 'Archives']`. | Default invalid category to `'Resources'`. |

---

### 2.4 Category 4: Vector Math & Auto-Linking Edge Cases

| ID | Edge Case Scenario | Risk Level | Expected System Behavior / Guardrail | Fallback Mechanism |
|---|---|---|---|---|
| **E4.1** | Zero-magnitude vector (empty text) | Low | `cosine_similarity()` checks `norm(a) == 0` or `norm(b) == 0`. | Return `0.0` similarity score immediately without division by zero. |
| **E4.2** | Single note in vault | Low | `process_auto_linking()` verifies `len(notes) >= 2`. | Skip link comparison loop; output "Only 1 note in vault." |
| **E4.3** | Duplicate inline `[[wikilink]]` insertion | Medium | `link.py` checks `if wikilink_str not in note_a.body` before appending. | Deduplicate frontmatter `links: []` using `set()`. |
| **E4.4** | `sentence-transformers` library missing | Medium | `load_model()` catches `ImportError` or download failure. | Fallback to deterministic TF-IDF / Hash vector embedder. |

---

### 2.5 Category 5: Graph Rendering & Streamlit UI Edge Cases

| ID | Edge Case Scenario | Risk Level | Expected System Behavior / Guardrail | Fallback Mechanism |
|---|---|---|---|---|
| **E5.1** | `data/graph.json` missing or empty | Low | Streamlit `app.py` checks `graph_html_path.exists()` and payload integrity. | Display info banner: "Graph not built. Click Process Pipeline." |
| **E5.2** | High node count (>500 nodes) | High | `vis-network` physics stabilization can lag. | Cap physics iterations at 150; enable `hideEdgesOnDrag`. |
| **E5.3** | Self-referencing link (A $\rightarrow$ A) | Low | `build_graph.py` ignores edges where `source == target`. | Filter out self-loops during JSON payload generation. |
| **E5.4** | Streamlit iframe height overflow | Low | Set explicit height parameter `components.html(..., height=550)`. | Provide scrollable container or expander wrapper. |

---

## 3. Data Integrity & Recovery Strategy

1. **State Recovery (`data/index.json`):** If `data/index.json` is corrupted or deleted, running `classify.py` automatically rebuilds the processing index by inspecting existing `wiki/**/*.md` files and matching `raw_id` fields.
2. **Vector Index Re-generation (`data/embeddings.pkl`):** If `data/embeddings.pkl` is missing or corrupted, `link.py` automatically re-computes 384-dim embeddings for all wiki notes and saves a clean pickle file.
3. **Graph JSON Re-generation (`data/graph.json`):** If `data/graph.json` is lost, `build_graph.py` regenerates the graph payload from the filesystem within under 2 seconds.
