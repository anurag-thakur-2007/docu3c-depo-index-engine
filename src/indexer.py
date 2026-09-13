import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from src.parser import extract_pdf_text

def build_vector_index(pdf_path: str, persist_directory: str = "./outputs/chroma_db"):
    """Parses a PDF, chunks the text, embeds it locally, and saves it to ChromaDB."""
    print(f"Step 1: Extracting text from {pdf_path}...")
    raw_text = extract_pdf_text(pdf_path)
    print(f"Extracted {len(raw_text)} characters successfully.")

    print("Step 2: Splitting text into overlapping chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.create_documents([raw_text])
    print(f"Created {len(docs)} text chunks.")

    print("Step 3: Initializing local Hugging Face embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print(f"Step 4: Storing embeddings into ChromaDB at '{persist_directory}'...")
    client = chromadb.PersistentClient(path=persist_directory)
    
    # Create or reset collection
    collection_name = "deposition_index"
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
        
    collection = client.create_collection(name=collection_name)

    # Extract text content and metadata
    texts = [doc.page_content for doc in docs]
    metadatas = [{"chunk_id": i} for i in range(len(docs))]
    ids = [f"chunk_{i}" for i in range(len(docs))]

    # Generate embeddings and add to collection in batches to manage memory
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_metadatas = metadatas[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        
        batch_embeddings = embeddings.embed_documents(batch_texts)
        
        collection.add(
            documents=batch_texts,
            embeddings=batch_embeddings,
            metadatas=batch_metadatas,
            ids=batch_ids
        )
        print(f"Indexed batch {i//batch_size + 1} / {(len(texts) + batch_size - 1)//batch_size}")

    print("Vector indexing complete! Database persisted successfully.")
    return collection

if __name__ == "__main__":
    target_pdf = os.path.join("data", "Persis_Yu_Deposition_Problem_statement.pdf")
    build_vector_index(target_pdf)