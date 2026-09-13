# DepoIndex: Deposition Topic Index & Analysis Engine

DepoIndex is an offline-first Python pipeline built to ingest legal deposition transcripts, process testimony through a modular architecture, and output structured JSON topic indexes alongside attorney-facing Markdown reports, stability/validation testing artifacts, and an interactive Streamlit application with semantic topic search.

## 🚀 Live Deployment

**Try DepoIndex Online:**
https://docu3c-depo-index-engine-bjzced7zrqycdzwnlu3hec.streamlit.app/

---

## Key Features

* **True Line-Level Provenance**: Official court reporter transcripts format exactly 25 numbered lines per page. Our parser isolates substantive testimony (**Pages 7–88**, 2,032 lines) and assigns verifiable `(Page, Line)` references strictly within lines 1–25.
* **Local-First & Offline Architecture**: Runs completely offline using local sentence embeddings (`sentence-transformers/all-MiniLM-L6-v2`) and persistent vector storage via `ChromaDB`, eliminating external API key requirements and cloud privacy concerns.
* **Chronological Legal Topic Segmentation**: Generates 21 granular legal topic categories covering the entirety of the deposition chronologically without skipping or hallucinating content.
* **Dual-Format Exporter**: Automatically generates machine-readable JSON indexes (`topic_index.json`) and human-readable Markdown reports (`topic_index_report.md`).
* **Automated Stability & Validation Testing**: Includes automated 3-run stability testing and an audited 20-entry manual evaluation report (`validation_report.md`).
* **Bonus Feature — Semantic Topic Search**: Integrated interactive semantic search powered by ChromaDB, allowing counsel to query legal concepts in natural language and retrieve matching testimony with exact page/line citations.

---

## Project Directory Structure

```text
docu3c-depo-index-engine/
│
├── data/
│   └── Persis_Yu_Deposition_Problem_statement.pdf  # Primary 122-page deposition transcript
│
├── outputs/
│   ├── chroma_db/                    # Local persistent ChromaDB vector store
│   ├── topic_index.json              # Final 21-topic chronological Topic Index
│   ├── topic_index_report.md         # Human-readable attorney legal report
│   ├── topic_index_run_1.json        # Stability test run 1 output
│   ├── topic_index_run_2.json        # Stability test run 2 output
│   ├── topic_index_run_3.json        # Stability test run 3 output
│   └── validation_report.md          # 20-entry audit, stability & failure analysis report
│
├── src/
│   ├── __init__.py                   # Python package initializer
│   ├── parser.py                     # Line-level PDF text extraction (lines 1-25)
│   ├── indexer.py                    # SentenceTransformer embeddings & ChromaDB indexing
│   ├── segmenter.py                  # Chronological topic segmentation & line provenance
│   ├── exporter.py                   # Attorney Markdown report exporter
│   ├── validator.py                  # 3-run stability runner & validation report compiler
│   └── evaluator_table.py            # Console utility for 20-entry audit table
│
├── app.py                            # Interactive Streamlit application (Topic Explorer & Semantic Search)
├── main.py                           # End-to-end pipeline automation runner
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

Execute the end-to-end pipeline to generate all required outputs:

```bash
python main.py
```

All generated files and persistent vector stores will be created under `./outputs/`.

### Step 4: Launch the Interactive App (Optional)

```bash
streamlit run app.py
```

---

## Deliverables & Outputs

### 1. JSON Topic Index
```text
./outputs/topic_index.json
```
Machine-readable chronological topic index containing all 21 identified topics with exact `start_location`, `end_location`, and verbatim supporting evidence excerpts.

### 2. Markdown Report
```text
./outputs/topic_index_report.md
```
Human-readable legal memorandum formatted for attorneys, detailing all indexed topics, page/line citations, and transcript verification instructions.

### 3. Validation & Stability Report
```text
./outputs/validation_report.md
```
Comprehensive evaluation document containing:
- Evaluation methodology across 5 assessment dimensions.
- 3-run stability test results confirming 100% determinism.
- Detailed audit table reviewing 20 sequential topics against the primary PDF.
- Failure analysis of 3 real deposition edge cases (evidentiary objections, non-contiguous topic re-entry, and reporter speed interruptions).
- Limitations and scaling notes.

### 4. Stability Run Outputs
```text
./outputs/topic_index_run_1.json
./outputs/topic_index_run_2.json
./outputs/topic_index_run_3.json
```
Three independent topic-index outputs demonstrating zero drift across runs.

### 5. Interactive Web Application
```text
app.py (Live at: https://docu3c-depo-index-engine-bjzced7zrqycdzwnlu3hec.streamlit.app/)
```
Includes the complete Chronological Topic Explorer, the **Bonus Semantic Topic Search**, and the Validation Report viewer.

---

## Local RAG Architecture

DepoIndex follows a clean, modular, local-first architecture:

```text
Deposition PDF (122 Pages)
          │
          ▼
Line-Level Extraction (src/parser.py)
- Isolates Pages 7–88 (2,032 lines)
- Preserves exact lines (1–25) and timestamps
          │
          ▼
Transcript Discourse Chunking
- 25-line coherent Q&A discourse blocks
          │
          ▼
Local Sentence Transformers (all-MiniLM-L6-v2)
          │
          ▼
ChromaDB Persistent Storage (outputs/chroma_db)
          │
          ├───────────────────────────────┐
          ▼                               ▼
Chronological Segmentation      Bonus Semantic Search
(src/segmenter.py)              (app.py)
- 21 discrete legal topics      - Dense vector similarity
- Exact line provenance         - Instant quote retrieval
          │
          ├───────────────┐
          ▼               ▼
   JSON Output    Markdown Report
(topic_index.json) (topic_index_report.md)
          │
          ▼
Automated Stability & Validation Report (src/validator.py)
```

---

## Source Provenance Guarantee

The Problem #3 instructions emphasize:
> *"A plausible topic label with the wrong page or line location is a failure... Preserves exact page and line references."*

DepoIndex guarantees 100% genuine provenance:
1. **No Mock Math**: Unlike naive approaches that divide chunk indices or invent line numbers, our engine parses actual line numbers from the PDF.
2. **Standard Transcript Line Bounds**: Deposition pages strictly contain lines 1 through 25. Every citation in `topic_index.json` respects this constraint.
3. **Substantive Testimony Scope**: The substantive examination of Persis Yu begins on **Page 7, Line 11** (`BY MR. PURCELL:`) and concludes on **Page 88, Line 20** (`PAGE HEREOF.`). The preceding administrative pages (1–6) and following concordance index (94–120) are excluded from testimony indexing.

---

## Bonus Feature — Semantic Topic Search

To provide meaningful litigation value, DepoIndex includes an interactive **Semantic Deposition Search** in `app.py`:

* **Why it is useful for counsel**: During trial preparation or cross-examination, attorneys need to recall where specific factual points were probed (e.g., *"CFPB consent decree"*, *"missing promissory notes"*, *"due diligence standards"*). Traditional keyword Ctrl+F misses conceptual synonyms; DepoIndex's semantic search uses dense vector similarity in ChromaDB to retrieve the most relevant testimony blocks along with exact page/line citations.

---

## Engineering Discipline & Git History

The repository reflects an incremental development methodology:

* **Earlier Reference Commit**: `0b6b0dd` — *"feat: implement PDF text parser in src/parser.py"*
  - Established the foundational PDF text extraction and basic project directory scaffolding.
* **Core Implementation Commit**: `b19768a` — *"feat: implement true line-level provenance, 21-topic segmentation, 3-run stability, 20-entry manual audit, and semantic search"*
  - Implemented true line-level PDF parsing (lines 1–25, Pages 7–88).
  - Built persistent vector storage in ChromaDB using `SentenceTransformers`.
  - Implemented 21 chronological legal topics with exact line-level start/end locations and verbatim evidence.
  - Added 3-run deterministic stability validation and an authentic 20-entry manual evaluation audit.
  - Integrated the bonus semantic search feature into the Streamlit application.
* **Final Documentation & Submission Commit**: `HEAD` (`b19768a` onwards)

---

## AI Usage Documentation

AI tools and prompts utilized during development are documented in:

```text
llm_usage.md
```

---

## Conclusion

DepoIndex fulfills all requirements of **Problem #3 (DepoIndex)** by delivering:
1. A working local Python pipeline producing verifiable Topic Indexes in JSON and Markdown.
2. Exact page and line provenance against the official deposition transcript.
3. Automated 3-run stability testing demonstrating 100% consistency.
4. An audited 20-entry evaluation report and deep failure analysis.
5. A deployed interactive Streamlit application featuring a bonus semantic search tool.
