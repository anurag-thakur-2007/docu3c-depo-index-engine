import streamlit as st
import json
import os

st.set_page_config(page_title="DepoIndex Engine", page_icon="📄", layout="wide")

st.title("📄 DepoIndex: Deposition Topic Indexer")
st.markdown("AI-Powered Legal Deposition Topic Segmentation & Provenance Tracker")

# Check if outputs exist
if os.path.exists("outputs/topic_index_report.md"):
    st.success("Pipeline outputs loaded successfully from local storage!")
    
    tab1, tab2, tab3 = st.tabs(["Attorney Report", "JSON Index", "Validation Report"])
    
    with tab1:
        st.subheader("Human-Readable Topic Index Report")
        with open("outputs/topic_index_report.md", "r", encoding="utf-8") as f:
            st.markdown(f.read())
            
    with tab2:
        st.subheader("Structured JSON Data")
        if os.path.exists("outputs/topic_index.json"):
            with open("outputs/topic_index.json", "r", encoding="utf-8") as f:
                st.json(json.load(f))
                
    with tab3:
        st.subheader("Validation & Stability Report")
        if os.path.exists("outputs/validation_report.md"):
            with open("outputs/validation_report.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
else:
    st.warning("⚠️ Pipeline outputs not found in `./outputs/`.")
    st.info("Please run your pipeline first using the button below or via your terminal (`python main.py`).")
    
    if st.button("Run Pipeline Now"):
        with st.spinner("Running main.py pipeline..."):
            exit_code = os.system("python main.py")
            if exit_code == 0:
                st.success("Pipeline executed successfully! Please refresh the page.")
                st.rerun()
            else:
                st.error("Pipeline execution failed. Check terminal logs.")