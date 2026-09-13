"""
Deposition Transcript Parser
Extracts line-by-line testimony from the deposition PDF while preserving
exact page numbers and transcript line numbers (lines 1 to 25).
"""

import os
import re
from pypdf import PdfReader


def extract_deposition_lines(pdf_path: str, start_page: int = 7, end_page: int = 88):
    """
    Parses substantive deposition testimony (Pages 7 to 88 of Persis Yu deposition).
    Extracts every numbered line, capturing the page number, line number (1-25),
    text content, and timestamp.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    reader = PdfReader(pdf_path)
    parsed_lines = []

    for p_num in range(start_page, min(end_page + 1, len(reader.pages) + 1)):
        page_text = reader.pages[p_num - 1].extract_text()
        if not page_text:
            continue

        for raw_line in page_text.split("\n"):
            line_str = raw_line.strip()
            # Ignore page footer markers or empty lines
            if not line_str or line_str == f"Page {p_num}":
                continue

            # Deposition lines follow: <line_number> <text> <optional timestamp>
            match = re.match(r"^(\d{1,2})\s+(.*?)(?:\s+(\d{2}:\d{2}))?$", line_str)
            if match:
                line_num = int(match.group(1))
                text_content = match.group(2).strip()
                timestamp = match.group(3) or ""
                
                # Verify standard deposition line bounds (1-25)
                if 1 <= line_num <= 25 and text_content:
                    parsed_lines.append({
                        "page": p_num,
                        "line": line_num,
                        "text": text_content,
                        "timestamp": timestamp
                    })

    return parsed_lines


def group_lines_into_blocks(lines, block_size: int = 25):
    """
    Groups transcript lines into coherent blocks (approx. 25 lines / 1 page per block)
    to facilitate embedding generation and semantic boundary detection while preserving
    exact line-level provenance for the start and end of every block.
    """
    blocks = []
    for i in range(0, len(lines), block_size):
        chunk_lines = lines[i:i + block_size]
        block_text = " ".join(item["text"] for item in chunk_lines)
        blocks.append({
            "block_id": len(blocks),
            "start_page": chunk_lines[0]["page"],
            "start_line": chunk_lines[0]["line"],
            "end_page": chunk_lines[-1]["page"],
            "end_line": chunk_lines[-1]["line"],
            "text": block_text,
            "lines": chunk_lines
        })
    return blocks


if __name__ == "__main__":
    pdf_file = os.path.join("data", "Persis_Yu_Deposition_Problem_statement.pdf")
    lines = extract_deposition_lines(pdf_file)
    blocks = group_lines_into_blocks(lines)
    print(f"Parsed {len(lines)} lines and created {len(blocks)} coherent transcript blocks.")
    print(f"Sample Line 1: Page {lines[0]['page']}, Line {lines[0]['line']}: {lines[0]['text']}")
    print(f"Sample Block 1 Range: Page {blocks[0]['start_page']}, Line {blocks[0]['start_line']} -> Page {blocks[0]['end_page']}, Line {blocks[0]['end_line']}")