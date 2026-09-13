# DepoIndex: Deposition Topic Index & Analysis Engine

DepoIndex is a local Python pipeline built to ingest legal deposition transcripts, process text through a modular architecture, and output structured JSON indexes alongside attorney-facing Markdown reports and stability/validation testing artifacts.

---

## Key Features

* **Local-First Architecture**: Runs offline using local sentence embeddings (`sentence-transformers/all-MiniLM-L6-v2`) and persistent vector storage via `ChromaDB`, avoiding external API key dependencies.
* **Modular Pipeline Design**: Separates concerns into dedicated modules for parsing (`parser.py`), indexing (`indexer.py`), segmentation (`segmenter.py`), reporting (`exporter.py`), and validation (`validator.py`).
* **Dual-Format Exporter**: Automatically generates machine-readable JSON indexes (`topic_index.json`) and human-readable Markdown reports (`topic_index_report.md`).
* **Automated Stability Testing**: Includes validation runners and evaluation reporting to test pipeline output consistency.

---

## Project Directory Structure

```text
docu3c-depo-index-engine/
│
├── data/
│   └── Persis_Yu_Deposition_Problem_statement.pdf
│
├── outputs/
│   ├── chroma_db/                    # Local persistent ChromaDB vector store
│   ├── topic_index.json              # Final chronological Topic Index (JSON)
│   ├── topic_index_report.md         # Human-readable attorney report (Markdown)
│   ├── topic_index_run_1.json        # Stability test run 1 output
│   ├── topic_index_run_2.json        # Stability test run 2 output
│   ├── topic_index_run_3.json        # Stability test run 3 output
│   └── validation_report.md          # Stability & evaluation report
│
├── src/
│   ├── __init__.py                   # Python package initializer
│   ├── parser.py                     # PDF text extraction and cleaning
│   ├── indexer.py                    # Embedding generation & ChromaDB storage
│   ├── segmenter.py                  # Chronological topic boundary detection
│   ├── exporter.py                   # Markdown report exporter
│   ├── validator.py                  # Stability testing & failure analysis
│   └── evaluator_table.py            # Evaluation table generator
│
├── main.py                            # End-to-end pipeline automation runner
├── requirements.txt                  # Python dependencies
├── llm_usage.md                      # AI tooling documentation
└── README.md                         # Project documentation
```

---

## Getting Started & Installation

### Prerequisites

* Python 3.12 or higher
* `pip`
* Git

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
cd docu3c-depo-index-engine
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Pipeline

Execute the root automation script to run the end-to-end pipeline and generate all required outputs:

```bash
python main.py
```

All generated files and databases will be stored inside the `./outputs/` directory.

---

## Deliverables & Outputs

1. **JSON Topic Index**
   `./outputs/topic_index.json`

2. **Markdown Report**
   `./outputs/topic_index_report.md`

3. **Validation & Stability Report**
   `./outputs/validation_report.md`

4. **Stability Run Outputs**
   `./outputs/topic_index_run_1.json`
   `./outputs/topic_index_run_2.json`
   `./outputs/topic_index_run_3.json`

---

## Engineering Discipline & Git History

* **Earlier Reference Commit**: `0b6b0dd`
* **Final Submission Commit**: The final commit SHA generated after the README is committed and pushed.

### Commit Evolution Summary

* **Earlier Commit**: Implemented the foundational PDF text parsing and modular project structure.
* **Final Commit**: Completed the end-to-end pipeline automation, local vector indexing, chronological topic segmentation, report generation, and stability testing.

---

## Technology Stack

| Component       | Technology                     |
| --------------- | ------------------------------ |
| Language        | Python 3.12+                   |
| Embeddings      | Sentence Transformers          |
| Embedding Model | `all-MiniLM-L6-v2`             |
| Vector Database | ChromaDB                       |
| Output Formats  | JSON / Markdown                |
| Architecture    | Local RAG Pipeline             |
| Testing         | Stability & Evaluation Testing |

---

## Local RAG Architecture

The pipeline uses a local Retrieval-Augmented Generation architecture:

```text
Deposition PDF
      │
      ▼
PDF Text Extraction
      │
      ▼
Text Cleaning & Provenance
      │
      ▼
Overlapping Chunking
      │
      ▼
Local Sentence Embeddings
      │
      ▼
ChromaDB Vector Store
      │
      ▼
Chronological Topic Segmentation
      │
      ▼
Topic Index
      │
      ├───────────────┐
      ▼               ▼
   JSON Output    Markdown Report
      │
      ▼
Validation & Stability Testing
```

The local architecture avoids dependency on paid external APIs and provides greater control over sensitive legal documents.

---

## Source Provenance

DepoIndex is designed to preserve traceability between generated topics and the original deposition transcript.

The indexing pipeline maintains source information including:

* PDF page numbers
* Transcript line ranges
* Source text/chunk references
* Chronological position

This allows each indexed topic to be traced back to its corresponding location in the original deposition transcript.

---

## Validation & Stability Testing

The project includes automated validation to evaluate pipeline consistency and output stability.

### Three-Run Stability Testing

The pipeline generates three independent outputs:

```text
topic_index_run_1.json
topic_index_run_2.json
topic_index_run_3.json
```

These outputs are used to evaluate consistency in:

* Topic ordering
* Topic boundaries
* Source provenance
* Missing or unexpected entries
* Overall output stability

### Manual Evaluation

A dedicated evaluation table is included to review generated topic-index entries for:

* Topic correctness
* Chronological ordering
* Source provenance accuracy
* Topic boundary quality
* Relevance of indexed content

The results are documented in:

```text
./outputs/validation_report.md
```

---

## AI Usage Documentation

Details regarding AI tools, prompts, development assistance, and validation are documented in:

```text
llm_usage.md
```

---

## Privacy & Security

DepoIndex follows a **local-first approach** for processing deposition material.

The core pipeline does not require sending deposition transcripts to external AI APIs. Embeddings and vector storage are generated locally using Sentence Transformers and ChromaDB.

This approach provides greater control over sensitive legal-document processing and reduces reliance on external services.

---

## Running the Project

From the repository root:

```bash
python main.py
```

Expected output structure:

```text
outputs/
├── chroma_db/
├── topic_index.json
├── topic_index_report.md
├── topic_index_run_1.json
├── topic_index_run_2.json
├── topic_index_run_3.json
└── validation_report.md
```

---

## Conclusion

DepoIndex provides an end-to-end pipeline for converting lengthy legal deposition transcripts into a structured, chronological, and verifiable topic index.

The project combines:

* Local RAG infrastructure
* Modular Python architecture
* Strict source provenance
* Chronological topic segmentation
* Structured JSON output
* Human-readable Markdown reporting
* Automated stability testing
* Manual evaluation

to provide a reproducible solution for legal deposition document analysis.

---

**Project:** DepoIndex
**Assessment:** Docu3C Technical Assessment — Problem #3
**Status:** Final Submission
