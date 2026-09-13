import streamlit as st
import json
import os

st.title("📄 DepoIndex: Deposition Topic Indexer")
st.markdown("AI-Powered Legal Deposition Topic Segmentation & Provenance Tracker")

# Check if outputs exist
if os.path.exists("outputs/topic_index_report.md"):
    st.success("Pipeline outputs loaded successfully!")
    
    tab1, tab2, tab3 = st.tabs(["Attorney Report", "JSON Index", "Validation Report"])
    
    with tab1:
        st.subheader("Human-Readable Topic Index Report")
        with open("outputs/topic_index_report.md", "r") as f:
            st.markdown(f.read())
            
    with tab2:
        st.subheader("Structured JSON Data")
        if os.path.exists("outputs/topic_index.json"):
            with open("outputs/topic_index.json", "r") as f:
                st.json(json.load(f))
                
    with tab3:
        st.subheader("Validation & Stability Report")
        if os.path.exists("outputs/validation_report.md"):
            with open("outputs/validation_report.md", "r") as f:
                st.markdown(f.read())
else:
    st.warning("Outputs not found. Run `python main.py` first.")