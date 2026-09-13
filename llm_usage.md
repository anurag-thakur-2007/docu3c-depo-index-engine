# LLM Usage Documentation

In accordance with the project submission guidelines, this document details how AI and LLM coding assistants were utilized during the development of the DepoIndex engine.

---

## 1. Scope of AI Assistance
* **Architecture & Scaffolding**: AI assistants were used to draft the modular project layout (`src/` separation of parser, indexer, segmenter, exporter, and validator).
* **Library Integration**: Provided syntax patterns for integrating local sentence embeddings (`sentence-transformers/all-MiniLM-L6-v2`) and persistent local `ChromaDB` instances without requiring paid external APIs.
* **Boilerplate Layouts**: Assisted in structuring output formats for the generated JSON indexes and Markdown reports.

---

## 2. Accepted, Modified, or Rejected Suggestions
* **Accepted**: The modular Python package approach using `src/` modules imported into a centralized `main.py` entry point.
* **Modified**: Adjusted text chunking and overlap parameters to better align with standard legal deposition line pagination.
* **Rejected**: Initial proposals suggesting cloud-based LLM API calls for real-time segmentation, as the project required a fully offline, self-contained local architecture.

---

## 3. Verification & Validation
* **Output Auditing**: Generated reports and outputs were manually checked to ensure formatting and structural integrity.
* **Local Reproducibility**: Verified that the entire pipeline executes locally from end-to-end via `python main.py` without external network or API dependencies.