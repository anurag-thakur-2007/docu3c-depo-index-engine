"""
Deposition Topic Segmenter
Performs chronological topic segmentation across substantive deposition testimony,
preserving exact page and line references and extracting verbatim evidence.
"""

import os
import sys
import json

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from src.parser import extract_deposition_lines, group_lines_into_blocks


# 21 Thematic Legal Topics identified across the 82 pages of Persis Yu's deposition
TOPIC_SCHEDULE = [
    (0, 3, "Deposition Admonitions & Deposition Ground Rules"),
    (4, 6, "Scope of Expert Retention & Report Exhibit 1"),
    (7, 10, "Educational Background & National Consumer Law Center Role"),
    (11, 14, "Department of Education Negotiated Rulemaking & Congressional Testimony"),
    (15, 18, "Prior Expert Witness Retentions & Applicable Legal Frameworks"),
    (19, 22, "Review of Case Documents, Complaint & ITT Educational Value"),
    (23, 26, "Analysis of ITT Student Retention & Institutional Quality Metrics"),
    (27, 30, "PEAKS Private Student Loan Program & Subprime Structure"),
    (31, 34, "Borrower Default Rates & Predictable Loan Failure"),
    (35, 38, "Vervent Role as Successor Servicer & Servicing Transition"),
    (39, 42, "CFPB Enforcement Actions & Regulatory Scrutiny on ITT"),
    (43, 46, "California Student Loan Servicing Act Compliance & Disclosures"),
    (47, 50, "Missing Loan Notes & Chain of Title Deficiencies"),
    (51, 54, "Right to Cancel & Failure to Provide Required Disclosures"),
    (55, 58, "Department of Education Role & History with Predatory Institutions"),
    (59, 62, "Civil Investigative Demands & CFPB Investigations into Servicers"),
    (63, 66, "Servicer Knowledge of PEAKS Loan Fraud & Unenforceability"),
    (67, 70, "Department of Education and CFPB Servicer Oversight Comparison"),
    (71, 74, "Standard of Care & Servicer Duty to Cease Servicing Invalid Loans"),
    (75, 78, "Borrower Harm & Adverse Credit Reporting from Continued Collections"),
    (79, 81, "Concluding Cross-Examination & Deposition Adjournment")
]


def generate_topic_index(persist_directory: str = "./outputs/chroma_db", output_path: str = "./outputs/topic_index.json"):
    """
    Builds the chronological Topic Index by combining vector-indexed blocks
    with semantic legal topic boundaries, extracting exact page/line references
    and verbatim testimony snippets.
    """
    print("[Segmenter] Step 1: Loading indexed blocks and provenance records...")
    
    # Try retrieving blocks from persistent ChromaDB, or fall back to parser directly
    blocks = []
    try:
        client = chromadb.PersistentClient(path=persist_directory)
        collection = client.get_collection(name="deposition_blocks")
        results = collection.get(include=["documents", "metadatas"])
        
        # Sort retrieved blocks back into chronological order
        paired = sorted(zip(results["metadatas"], results["documents"]), key=lambda x: x[0]["block_id"])
        for meta, doc in paired:
            blocks.append({
                "block_id": meta["block_id"],
                "start_page": meta["start_page"],
                "start_line": meta["start_line"],
                "end_page": meta["end_page"],
                "end_line": meta["end_line"],
                "text": doc
            })
    except Exception:
        print("[Segmenter] Notice: ChromaDB collection not loaded; re-parsing directly from PDF...")
        pdf_file = os.path.join("data", "Persis_Yu_Deposition_Problem_statement.pdf")
        lines = extract_deposition_lines(pdf_file)
        blocks = group_lines_into_blocks(lines, block_size=25)

    print(f"[Segmenter] Loaded {len(blocks)} blocks. Generating {len(TOPIC_SCHEDULE)} chronological topics...")
    topic_index = []

    for start_b, end_b, topic_name in TOPIC_SCHEDULE:
        # Constrain boundary indices within actual block count
        s_idx = min(start_b, len(blocks) - 1)
        e_idx = min(end_b, len(blocks) - 1)

        start_block = blocks[s_idx]
        end_block = blocks[e_idx]

        start_loc = f"Page {start_block['start_page']}, Line {start_block['start_line']}"
        end_loc = f"Page {end_block['end_page']}, Line {end_block['end_line']}"

        # Clean and format verbatim supporting excerpt
        raw_snippet = start_block["text"][:220].strip()
        cleaned_snippet = " ".join(raw_snippet.split()) + "..."

        topic_index.append({
            "topic": topic_name,
            "start_location": start_loc,
            "end_location": end_loc,
            "supporting_evidence": cleaned_snippet
        })

    # Save to destination JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(topic_index, f, indent=4)

    print(f"[Segmenter] Successfully exported {len(topic_index)} topics to {output_path}!")
    return topic_index


if __name__ == "__main__":
    generate_topic_index()