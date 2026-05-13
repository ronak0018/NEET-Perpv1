"""Quick test of the parsers without MongoDB."""
import re
import os
import sys

# Add parent dir
sys.path.insert(0, os.path.dirname(__file__))
from seed_from_pdfs import parse_pyqs_2024, parse_recall_2025

pdf_text_path = os.path.join(os.path.dirname(__file__), "pdf_extracted.txt")
with open(pdf_text_path, "r", encoding="utf-8") as f:
    full_text = f.read()

file_sections = re.split(r'={80}\nFILE: .+\n={80}', full_text)
file_names = re.findall(r'={80}\nFILE: (.+)\n={80}', full_text)

for name, section in zip(file_names, file_sections[1:]):
    if "PYQs-2024" in name:
        print(f"Parsing: {name}")
        qs = parse_pyqs_2024(section)
        print(f"  Found {len(qs)} questions")
        if qs:
            print(f"  Sample: {qs[0]['subject']} - {qs[0]['question'][:80]}...")
            print(f"  Options: {qs[0]['options']}")
            print(f"  Correct: {qs[0]['correct_answer']}")
    elif "Recall-Questions-2025" in name:
        print(f"Parsing: {name}")
        qs = parse_recall_2025(section)
        print(f"  Found {len(qs)} questions")
        # Show subject distribution
        subjects = {}
        for q in qs:
            subjects[q["subject"]] = subjects.get(q["subject"], 0) + 1
        print("  Subject distribution:")
        for s, c in sorted(subjects.items()):
            print(f"    {s}: {c}")
        # Show a Medicine sample
        med_qs = [q for q in qs if q["subject"] == "Medicine"]
        if med_qs:
            print(f"\n  Medicine sample:")
            print(f"    Q: {med_qs[0]['question'][:100]}...")
            print(f"    Opts: {[o[:50] for o in med_qs[0]['options']]}")
