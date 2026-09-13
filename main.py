import os
from src.indexer import build_vector_index
from src.segmenter import generate_topic_index
from src.exporter import export_to_markdown
from src.validator import run_stability_and_validation_tests

if __name__ == "__main__":
    print("=== Starting Full DepoIndex Pipeline ===")
    target_pdf = os.path.join("data", "Persis_Yu_Deposition_Problem_statement.pdf")
    
    # 1. Indexing PDF into ChromaDB
    build_vector_index(target_pdf)
    
    # 2. Segmenting Topics
    generate_topic_index()
    
    # 3. Exporting Markdown Report
    export_to_markdown()
    
    # 4. Running Stability Tests & Validation Report
    run_stability_and_validation_tests()
    
    print("\n=== Pipeline Complete! All outputs generated successfully in ./outputs/ ===")