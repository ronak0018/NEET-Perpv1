"""Find subject headers in the Recall 2025 section."""

with open(r'c:\Ronak-EY\Non-GIT\Neet-PG\pdf_extracted.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the Recall 2025 section
recall_start = text.find('FILE: NEET-PG-Recall-Questions-2025.pdf')
if recall_start == -1:
    print("Recall 2025 section not found!")
else:
    recall_text = text[recall_start:]
    lines = recall_text.split('\n')
    
    # Look for standalone subject headers (short lines that could be subjects)
    import re
    subjects_found = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Subject headers are typically 1-3 words on their own line
        if stripped and len(stripped) < 40 and not stripped.startswith('Q.') and not stripped.startswith('A.') and not stripped.startswith('B.') and not stripped.startswith('C.') and not stripped.startswith('D.') and not stripped.startswith('---') and not stripped.startswith('='):
            subject_match = re.match(
                r'^(Anatomy|Physiology|Biochemistry|Pathology|Pharmacology|'
                r'Microbiology|Forensic\s*Medicine|FMT|PSM|SPM|Community\s*Medicine|'
                r'Medicine|Surgery|Obstetrics|Gynaecology|OBG|Obs\s*&\s*Gyn|'
                r'Obs\s+and\s+Gyn|Paediatrics|Pediatrics|ENT|Ophthalmology|'
                r'Radiology|Anaesthesia|Anesthesia|Ortho(?:paedics)?|'
                r'Psychiatry|Derma(?:tology)?|Preventive\s+Medicine|'
                r'Obstetrics\s+(?:and|&)\s+Gynaecology|'
                r'General\s+Medicine|General\s+Surgery)\s*$',
                stripped, re.IGNORECASE
            )
            if subject_match:
                subjects_found.append((i, stripped))
    
    print(f"Subject headers found in Recall 2025:")
    for line_num, subj in subjects_found:
        print(f"  Line {line_num}: '{subj}'")
    
    # Count Q. lines
    q_count = sum(1 for l in lines if l.strip().startswith('Q.'))
    print(f"\nTotal Q. lines: {q_count}")
