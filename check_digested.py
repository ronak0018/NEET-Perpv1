import os, re

NOTES_DIR = os.path.join(os.path.dirname(__file__), "Files", "Master-notes")

SUBJECT_MAP = {
    "anatomy": "Anatomy",
    "surgery": "Surgery",
    "radiology": "Radiology",
    "psychiatry": "Psychiatry",
    "anaesthesia_neet_pg_study_notes": "Anaesthesia",
    "physiology_neet_pg_study_notes": "Physiology",
    "pharmacology_neet_pg_study_notes": "Pharmacology",
}

def extract_subject(filename):
    stem = re.sub(r"\.(md|txt)$", "", filename.lower())
    return SUBJECT_MAP.get(stem, stem.replace("_", " ").title())

# Mimic seed logic: prefer .md over .txt for same subject
all_files = sorted([f for f in os.listdir(NOTES_DIR) if f.endswith(".txt") or f.endswith(".md")])
files_by_subject = {}
for fname in all_files:
    subject = extract_subject(fname)
    if subject in files_by_subject:
        if fname.endswith(".md"):
            files_by_subject[subject] = fname
    else:
        files_by_subject[subject] = fname

print(f"\n=== Master Notes Digestion Report ===")
print(f"Total files in Master-notes folder: {len(all_files)}")
print(f"Unique subjects (after dedup): {len(files_by_subject)} / 20 files")
print(f"\nDigested subjects ({len(files_by_subject)}):")
for subj, fname in sorted(files_by_subject.items()):
    print(f"  + {subj:<45} <- {fname}")
