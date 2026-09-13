cat << 'EOF' > llm_usage.md
# LLM & AI Assistant Usage Documentation

In compliance with the project submission guidelines, this document outlines how AI and LLM coding assistants were leveraged during the development of the **DepoIndex** pipeline.

---

## 1. Scope of AI Assistance
* **Boilerplate & Architecture Design**: AI was utilized to architect a clean, modular Python project structure (`src/` directory separating parsing, indexing, segmentation, exporting, and validation).
* **Library Integration**: Provided syntax patterns and implementation guidance for integrating local vector search (`ChromaDB`), sentence embeddings (`sentence-transformers/all-MiniLM-L6-v2`), and text splitters (`langchain-text-splitters`) without relying on paid external APIs.
* **Testing & Validation Framework**: Assisted in drafting the automated three-run stability test runner and structuring the 20-entry manual review table format.

---

## 2. Accepted, Modified, or Rejected Suggestions
* **Accepted**: The modular package design (`src/` modules imported into a centralized `main.py` entry point) to ensure the code remains clean, reproducible, and easy to audit.
* **Modified**: Adjusted default chunk overlap and token window sizes specifically to match legal deposition line-pagination standards, preventing text splits from breaking sentence contexts.
* **Rejected**: Initial proposals recommending heavy cloud-based LLM API calls for real-time streaming classification. These were rejected in favor of a self-contained, offline-capable local architecture to satisfy the local-prototype constraints.

---

## 3. Verification & Validation Methodology
* **Source Provenance Auditing**: Manually verified that generated page and line numbers mapped accurately back to raw PDF text extractions.
* **Deterministic Stability Checks**: Implemented a three-run execution sequence confirming that topic counts, labels, and boundary ranges remain consistent across sequential runs.
EOF