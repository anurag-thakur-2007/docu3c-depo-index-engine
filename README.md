# DepoIndex: AI-Powered Deposition Topic Index Engine

DepoIndex is a professional-grade, locally running **RAG-based pipeline** engineered to solve **Problem #3** of the Docu3C technical assessment.

It ingests complex legal deposition transcripts, segments them chronologically into meaningful legal topics, preserves strict page/line source provenance, and outputs both structured JSON indexes and human-readable Markdown reports alongside automated validation and stability test reports.

---

## Key Features

* **Local-First Architecture**
  Runs entirely offline using local vector embeddings with `sentence-transformers/all-MiniLM-L6-v2` and persistent vector storage using `ChromaDB`. This removes the need for paid API keys or complex cloud deployments.

* **Strict Source Provenance**
  Maintains exact page and line addressability from raw PDF extraction through chunking and topic indexing, allowing attorneys to verify every entry against the original testimony.

* **Automated Stability & Validation Testing**
  Includes built-in three-run stability testing and a 20-entry manual review evaluation to assess reliability, consistency, and deterministic outputs.

* **Dual-Format Exporter**
  Automatically generates:

  * Machine-readable JSON: `topic_index.json`
  * Human-readable Markdown: `topic_index_report.md`

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
│   ├── topic_index.json              # Final chronological Topic Index
│   ├── topic_index_report.md         # Human-readable attorney report
│   ├── topic_index_run_1.json        # Stability test run 1 output
│   ├── topic_index_run_2.json        # Stability test run 2 output
│   ├── topic_index_run_3.json        # Stability test run 3 output
│   └── validation_report.md          # Stability & validation report
│
├── src/
│   ├── __init__.py                   # Python package initializer
│   ├── parser.py                     # PDF text extraction and cleaning
│   ├── indexer.py                    # Embedding generation & ChromaDB storage
│   ├── segmenter.py                  # Chronological topic boundary detection
│   ├── exporter.py                   # Markdown report exporter
│   ├── validator.py                  # Stability testing & failure analysis
│   └── evaluator_table.py             # 20-entry manual review table generator
│
├── main.py                            # End-to-end pipeline automation runner
├── requirements.txt                   # Python dependencies
├── llm_usage.md                       # AI tools, prompts, and validation documentation
└── README.md                          # Project documentation
```

---

## Getting Started

### Prerequisites

Make sure the following is installed:

* **Python 3.12 or higher**
* `pip`
* Git

---

## Installation

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
cd docu3c-depo-index-engine
```

### Step 2: Install Dependencies

Install all required Python libraries specified in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Run the End-to-End Pipeline

Execute the root automation script:

```bash
python main.py
```

The pipeline will:

1. Parse the deposition PDF.
2. Extract and clean the transcript text.
3. Preserve page and line-level provenance.
4. Create overlapping text chunks.
5. Generate local vector embeddings.
6. Store embeddings in ChromaDB.
7. Detect chronological topic boundaries.
8. Generate the topic index.
9. Export the JSON topic index.
10. Generate the human-readable Markdown report.
11. Run three stability test executions.
12. Generate the validation and manual review report.

All generated artifacts and databases are stored inside the:

```text
./outputs/
```

directory.

---

## Deliverables & Output Verification

After successfully running the pipeline, the following deliverables will be generated.

### 1. JSON Topic Index

```text
./outputs/topic_index.json
```

Contains the final chronological topic index in a structured, machine-readable format.

### 2. Human-Readable Markdown Report

```text
./outputs/topic_index_report.md
```

Contains an attorney-facing representation of the indexed deposition topics, including their source provenance.

### 3. Validation & Stability Report

```text
./outputs/validation_report.md
```

Contains:

* 20-entry manual review evaluation
* Evaluation methodology
* Three-run stability test results
* Failure analysis
* Reliability observations
* Validation outcomes

### 4. Stability Test Outputs

```text
./outputs/topic_index_run_1.json
./outputs/topic_index_run_2.json
./outputs/topic_index_run_3.json
```

These files contain the outputs from three independent pipeline executions and are used to evaluate output stability and consistency.

---

## Source Provenance

A core design goal of DepoIndex is maintaining **traceability between generated topics and the original deposition transcript**.

Each indexed topic preserves source information such as:

* PDF page number
* Transcript line range
* Source text/chunk reference
* Chronological position

This allows users to move from a generated topic directly back to the relevant portion of the original deposition.

The provenance pipeline follows this general flow:

```text
Original PDF
     │
     ▼
PDF Text Extraction
     │
     ▼
Page & Line Preservation
     │
     ▼
Text Cleaning
     │
     ▼
Overlapping Chunking
     │
     ▼
Local Embeddings
     │
     ▼
ChromaDB
     │
     ▼
Topic Segmentation
     │
     ▼
Chronological Topic Index
     │
     ├───────────────┐
     ▼               ▼
JSON Output      Markdown Report
     │
     ▼
Validation & Stability Testing
```

---

## Local RAG Architecture

DepoIndex follows a local-first Retrieval-Augmented Generation architecture.

### Embedding Model

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

for generating vector representations of deposition transcript chunks.

### Vector Database

The generated embeddings are stored in:

```text
ChromaDB
```

with persistent local storage under:

```text
./outputs/chroma_db/
```

### Benefits

The local architecture provides:

* No paid API keys
* No external cloud dependency
* Reproducible local execution
* Better control over sensitive legal documents
* Persistent vector storage
* Easier evaluation and testing

---

## Topic Segmentation

The segmentation engine is designed to identify meaningful changes in deposition subject matter while preserving the original chronological order.

Rather than producing an unordered collection of topics, DepoIndex maintains the sequence in which topics occur in the deposition.

The resulting structure is conceptually:

```text
Topic 1
  ├── Page / Line Provenance
  └── Relevant Transcript Content

Topic 2
  ├── Page / Line Provenance
  └── Relevant Transcript Content

Topic 3
  ├── Page / Line Provenance
  └── Relevant Transcript Content

...
```

This makes the generated index useful for reviewing long deposition transcripts efficiently.

---

## Validation & Stability Testing

DepoIndex includes an automated validation framework to evaluate the consistency of the pipeline.

### Three-Run Stability Test

The complete pipeline is executed three times and produces:

```text
topic_index_run_1.json
topic_index_run_2.json
topic_index_run_3.json
```

The outputs are compared to identify:

* Topic ordering changes
* Topic boundary changes
* Provenance inconsistencies
* Missing entries
* Unexpected output variations

### 20-Entry Manual Review

The project also includes a 20-entry manual evaluation table.

The review focuses on factors such as:

* Topic correctness
* Chronological ordering
* Source provenance accuracy
* Topic boundary quality
* Relevance of indexed content

The resulting evaluation is incorporated into:

```text
./outputs/validation_report.md
```

---

## Engineering Discipline & Git History

The project was d
