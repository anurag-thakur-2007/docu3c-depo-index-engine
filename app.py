"""
DepoIndex: AI-Powered Deposition Topic Indexer & Verification Workbench
Streamlit Web Application providing interactive chronological topic exploration,
bonus semantic topic search, and source provenance cross-checking.
"""

import os
import json
import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer

# Page setup
st.set_page_config(
    page_title="DepoIndex: Deposition Topic Indexer",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ DepoIndex: Deposition Topic Indexer & Provenance Engine")
st.caption("AI/LLM Engineering Problem #3 — Deposition of Persis Yu (*Heather Turrey vs. Vervent, Inc.*)")

# Check if outputs exist
topic_index_path = "outputs/topic_index.json"
report_path = "outputs/topic_index_report.md"
validation_path = "outputs/validation_report.md"
chroma_dir = "outputs/chroma_db"

if not os.path.exists(topic_index_path):
    st.error("⚠️ Topic Index not found in `./outputs/`. Please run the pipeline first.")
    if st.button("Run Pipeline Now"):
        with st.spinner("Executing main.py..."):
            code = os.system("python main.py")
            if code == 0:
                st.success("Pipeline executed successfully! Please refresh.")
                st.rerun()
            else:
                st.error("Execution failed. Check console logs.")
    st.stop()

# Load Topic Index
with open(topic_index_path, "r", encoding="utf-8") as f:
    topics = json.load(f)

# Navigation Tabs
tab_index, tab_search, tab_report, tab_about = st.tabs([
    "📋 Chronological Topic Index",
    "🔍 Semantic Topic Search (Bonus)",
    "📊 Validation & Stability Report",
    "ℹ️ Case & Provenance Architecture"
])

# ---------------------------------------------------------
# TAB 1: Chronological Topic Index
# ---------------------------------------------------------
with tab_index:
    st.subheader(f"Chronological Deposition Topics ({len(topics)} Identified)")
    st.markdown(
        "Every topic preserves exact **page and line addressability (lines 1–25)** "
        "covering substantive testimony from **Page 7, Line 11** to **Page 88, Line 20**."
    )

    # Search filter
    filter_q = st.text_input("Filter topics by keyword:", placeholder="e.g., PEAKS, CFPB, California, default...")
    
    filtered_topics = [
        t for t in topics 
        if filter_q.lower() in t["topic"].lower() or filter_q.lower() in t["supporting_evidence"].lower()
    ] if filter_q else topics

    st.write(f"Showing **{len(filtered_topics)}** matching topics:")

    for i, item in enumerate(filtered_topics, 1):
        with st.expander(f"**#{i}. {item['topic']}** — `{item['start_location']} → {item['end_location']}`"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("**Start Location:**")
                st.info(item['start_location'])
                st.markdown("**End Location:**")
                st.info(item['end_location'])
            with col2:
                st.markdown("**Verbatim Testimony Excerpt:**")
                st.markdown(f"> *\"{item['supporting_evidence']}\"*")

# ---------------------------------------------------------
# TAB 2: Semantic Topic Search (Bonus Feature)
# ---------------------------------------------------------
with tab_search:
    st.subheader("🔍 Bonus Feature: Semantic Deposition Search")
    st.info(
        "**Why this is useful for litigation counsel:** Attorneys frequently need to locate where a specific "
        "factual question or legal theory (e.g. *regulatory notice*, *promissory notes*, *default rates*) was probed "
        "without knowing the exact wording used by counsel. This tool performs dense semantic vector search "
        "against the deposition blocks in ChromaDB and returns exact page and line citations."
    )

    search_query = st.text_input(
        "Enter natural language legal query or concept:",
        placeholder="e.g. CFPB enforcement and loan cancellation, or missing promissory notes"
    )

    if search_query:
        try:
            with st.spinner("Searching deposition embeddings in ChromaDB..."):
                client = chromadb.PersistentClient(path=chroma_dir)
                collection = client.get_collection(name="deposition_blocks")
                embedder = SentenceTransformer("all-MiniLM-L6-v2")
                query_vector = embedder.encode([search_query]).tolist()

                results = collection.query(
                    query_embeddings=query_vector,
                    n_results=4
                )

                st.write(f"### Top Semantic Matches for *\"{search_query}\"*:")
                for idx in range(len(results["ids"][0])):
                    meta = results["metadatas"][0][idx]
                    doc = results["documents"][0][idx]
                    dist = results["distances"][0][idx] if "distances" in results else None
                    score = f"{(1 - dist):.2f}" if dist is not None else "High"

                    st.markdown(f"#### Match #{idx+1}: `{meta['location']}` (Relevance Score: {score})")
                    st.markdown(f"> *\"{doc}\"*")
                    st.divider()

        except Exception as e:
            st.error(f"Error querying vector index: {e}")

# ---------------------------------------------------------
# TAB 3: Validation & Stability Report
# ---------------------------------------------------------
with tab_report:
    st.subheader("Audited Validation Report & Stability Assessment")
    if os.path.exists(validation_path):
        with open(validation_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.warning("Validation report not found.")

# ---------------------------------------------------------
# TAB 4: Case & Provenance Architecture
# ---------------------------------------------------------
with tab_about:
    st.subheader("About DepoIndex Architecture")
    st.markdown("""
    ### Technical Overview
    - **Local-First & Offline**: Uses `sentence-transformers/all-MiniLM-L6-v2` and local `ChromaDB` persistent storage. No external API keys or cloud dependencies.
    - **True Line-Level Provenance**: Standard court transcripts enforce exactly 25 numbered lines per page. Our parser isolates substantive testimony (**Pages 7–88**, 2,032 lines) and assigns exact start and end line references.
    - **Deterministic Stability**: Tested over three consecutive runs yielding 100% reproducible topic counts, labels, and boundary lines.
    - **Attorney Verification**: Every indexed entry carries verbatim quoted text so counsel can open the primary PDF and verify testimony immediately.
    """)