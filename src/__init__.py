"""
DepoIndex Engine Package
Modular pipeline for legal deposition topic indexing, line-level provenance tracking,
and automated validation.
"""

from src.parser import extract_deposition_lines, group_lines_into_blocks
from src.indexer import build_vector_index
from src.segmenter import generate_topic_index
from src.exporter import export_to_markdown
from src.validator import run_stability_and_validation_tests

__all__ = [
    "extract_deposition_lines",
    "group_lines_into_blocks",
    "build_vector_index",
    "generate_topic_index",
    "export_to_markdown",
    "run_stability_and_validation_tests",
]
