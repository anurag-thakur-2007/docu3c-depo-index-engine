"""
Deposition Vector Indexer
Ingests parsed transcript blocks, computes local sentence embeddings using
SentenceTransformers, and stores them in ChromaDB with exact line-level metadata.
"""

import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from sentence_transformers import SentenceTransformer
from src.parser import extract_deposition_lines, group_lines_into_blocks


def build_vector_index(pdf_path: str = None, persist_directory: str = "./outputs/chroma_db"):
    """
    Parses substantive deposition testimony, groups into blocks with line-level provenance,
    generates embeddings with all-MiniLM-L6-v2, and indexes into ChromaDB.
    """
    if pdf_path is None:
        pdf_path = os.path.join("data", "Persis_Yu_Deposition_Problem_statement.pdf")

    print(f"[Indexer] Step 1: Parsing deposition lines from {pdf_path}...")
    lines = extract_deposition_lines(pdf_path)
    blocks = group_lines_into_blocks(lines, block_size=25)
    print(f"[Indexer] Extracted {len(lines)} lines and created {len(blocks)} transcript blocks.")

    print("[Indexer] Step 2: Loading local SentenceTransformer model (all-MiniLM-L6-v2)...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    print(f"[Indexer] Step 3: Initializing persistent ChromaDB at {persist_directory}...")
    os.makedirs(persist_directory, exist_ok=True)
    client = chromadb.PersistentClient(path=persist_directory)

    collection_name = "deposition_blocks"
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = client.create_collection(name=collection_name)

    texts = [b["text"] for b in blocks]
    ids = [f"block_{b['block_id']}" for b in blocks]
    metadatas = [{
        "block_id": b["block_id"],
        "start_page": b["start_page"],
        "start_line": b["start_line"],
        "end_page": b["end_page"],
        "end_line": b["end_line"],
        "location": f"Page {b['start_page']}, Line {b['start_line']} - Page {b['end_page']}, Line {b['end_line']}"
    } for b in blocks]

    print("[Indexer] Step 4: Computing embeddings and populating vector store...")
    embeddings = embedder.encode(texts, show_progress_bar=False).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"[Indexer] Successfully indexed {len(blocks)} blocks into ChromaDB!")
    return collection, blocks


if __name__ == "__main__":
    build_vector_index()