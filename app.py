"""Unified Streamlit interface for capture, search, and graph exploration."""

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from ask import ask
from capture import capture_file, capture_link, capture_note
from lib.storage import GRAPH_FILE, PROJECT_ROOT, STATIC_DIR, read_raw_captures, read_wiki_notes
from pipeline import run_pipeline


st.set_page_config(
    page_title="SecondSelf - Personal AI Second Brain",
    page_icon="brain",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white; border: none; border-radius: 6px; font-weight: 600;
    }
    .source-card {
        background: #161b22; border-left: 3px solid #2563eb;
        padding: .75rem 1rem; border-radius: 4px; margin-bottom: .5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=5)
def get_vault_stats():
    graph_nodes = graph_edges = 0
    if GRAPH_FILE.exists():
        try:
            graph = json.loads(GRAPH_FILE.read_text(encoding="utf-8"))
            metadata = graph.get("metadata", {})
            graph_nodes = metadata.get("node_count", len(graph.get("nodes", [])))
            graph_edges = metadata.get("edge_count", len(graph.get("edges", [])))
        except (OSError, json.JSONDecodeError):
            pass
    return len(read_raw_captures()), len(read_wiki_notes()), graph_nodes, graph_edges


def graph_html() -> str:
    html_path = STATIC_DIR / "graph.html"
    if not html_path.exists():
        return ""
    html = html_path.read_text(encoding="utf-8")
    graph_data = {}
    if GRAPH_FILE.exists():
        try:
            graph_data = json.loads(GRAPH_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            graph_data = {}
    return html.replace(
        "window.SECONDSELF_GRAPH_DATA = null;",
        "window.SECONDSELF_GRAPH_DATA = " + json.dumps(graph_data, ensure_ascii=False).replace("<", "\\u003c") + ";",
    )


st.title("SecondSelf - Personal AI Second Brain")
st.caption("Local-first capture, structured PARA wiki, vector retrieval, and knowledge graph.")
raw_count, wiki_count, node_count, edge_count = get_vault_stats()
columns = st.columns(4)
columns[0].metric("Raw Captures", raw_count)
columns[1].metric("Wiki Pages", wiki_count)
columns[2].metric("Graph Nodes", node_count)
columns[3].metric("Graph Edges", edge_count)

st.divider()
st.subheader("Ask Your Brain")
query = st.text_input(
    "Ask a question over your accumulated knowledge:",
    placeholder="What are the core goals of SecondSelf?",
)
if st.button("Ask Question", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching and synthesizing from the vault..."):
            result = ask(query.strip())
        st.markdown("### Answer")
        st.info(result.answer)
        if result.sources:
            st.markdown("### Sources")
            for source in result.sources:
                st.markdown(
                    "<div class='source-card'><strong>[{}]</strong> ({}) - relevance {}<br/><em>{}</em></div>".format(
                        source["id"], source["para"], source["relevance_score"], source["summary"]
                    ),
                    unsafe_allow_html=True,
                )

st.divider()
st.subheader("Interactive Knowledge Graph")
content = graph_html()
if content:
    components.html(content, height=550, scrolling=False)
else:
    st.info("No graph has been generated yet. Run the pipeline from the sidebar.")

with st.sidebar:
    st.header("Ingest Content")
    tab_note, tab_link, tab_file = st.tabs(["Note", "Link", "File"])

    with tab_note:
        note_input = st.text_area("Note content:", height=120)
        if st.button("Save Note"):
            try:
                result = capture_note(note_input)
                st.success(f"Saved raw/{result.id}")
                st.cache_data.clear()
            except (ValueError, OSError) as exc:
                st.error(str(exc))

    with tab_link:
        url_input = st.text_input("URL:")
        link_notes = st.text_input("Optional notes:")
        if st.button("Save Link"):
            try:
                result = capture_link(url_input, notes=link_notes)
                st.success(f"Saved raw/{result.id}")
                st.cache_data.clear()
            except (ValueError, OSError) as exc:
                st.error(str(exc))

    with tab_file:
        uploaded = st.file_uploader("Choose a PDF, Markdown, or text file:")
        if st.button("Save Uploaded File"):
            if uploaded is None:
                st.error("Please select a file.")
            else:
                try:
                    safe_name = Path(uploaded.name).name or "upload.bin"
                    scratch_dir = PROJECT_ROOT / "data" / "uploads"
                    scratch_dir.mkdir(parents=True, exist_ok=True)
                    temp_path = scratch_dir / safe_name
                    temp_path.write_bytes(uploaded.getbuffer())
                    result = capture_file(str(temp_path))
                    st.success(f"Saved {safe_name} as raw/{result.id}")
                    st.cache_data.clear()
                except (ValueError, OSError) as exc:
                    st.error(str(exc))

    st.divider()
    if st.button("Process Pipeline and Rebuild Graph", use_container_width=True):
        try:
            with st.spinner("Classifying, linking, and rebuilding graph..."):
                summary = run_pipeline("process")
            st.cache_data.clear()
            st.success(
                "Processed {} captures, added {} links, graph: {} nodes / {} edges.".format(
                    summary["classified"], summary["links_added"], summary["graph_nodes"], summary["graph_edges"]
                )
            )
            st.rerun()
        except Exception as exc:
            st.error(f"Pipeline failed: {exc}")
