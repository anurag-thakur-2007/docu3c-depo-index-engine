import os
from pypdf import PdfReader

def extract_pdf_text(pdf_path: str) -> str:
    """Extracts all text from a given PDF file path page by page."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    extracted_text = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            extracted_text.append(f"--- Page {i + 1} ---\n{text}")
            
    return "\n\n".join(extracted_text)

if __name__ == "__main__":
    # Test parser with your deposition file
    target_pdf = os.path.join("data", "Persis_Yu_Deposition_Problem_statement.pdf")
    print(f"Loading PDF from: {target_pdf}")
    
    try:
        doc_text = extract_pdf_text(target_pdf)
        print(f"Successfully extracted {len(doc_text)} characters.")
        print("\n--- Preview (First 300 characters) ---")
        print(doc_text[:300])
    except Exception as e:
        print(f"Error extracting text: {e}")