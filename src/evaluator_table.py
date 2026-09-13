"""
Evaluation Table Generator
Utility script to display the audited 20-entry evaluation breakdown for verification.
"""

import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.validator import AUDIT_ENTRIES


def display_evaluation_table():
    """
    Prints the 20 audited entries directly to the console in a structured table.
    """
    print("=" * 80)
    print("DEPOINDEX: 20-ENTRY MANUAL AUDIT & PROVENANCE TABLE")
    print("=" * 80)
    print(f"{'ID':<4} | {'Topic Title':<45} | {'Location':<30} | {'Acc':<6}")
    print("-" * 80)
    for item in AUDIT_ENTRIES:
        print(f"{item['id']:<4} | {item['topic'][:45]:<45} | {item['location']:<30} | {item['loc_acc']:<6}")
    print("=" * 80)
    print(f"Total audited entries: {len(AUDIT_ENTRIES)}")


if __name__ == "__main__":
    display_evaluation_table()