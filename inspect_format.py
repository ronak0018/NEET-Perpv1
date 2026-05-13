"""Inspect the format of questions in the extracted PDF text."""

with open(r'c:\Ronak-EY\Non-GIT\Neet-PG\pdf_extracted.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find Recall 2025 section
print("=== RECALL 2025 FORMAT ===")
for i, line in enumerate(lines):
    if 'NEET-PG-Recall-Questions-2025' in line:
        print(f'Recall 2025 starts at line {i+1}')
        for j in range(i, min(i+120, len(lines))):
            print(f'{j+1}: {lines[j]}', end='')
        break

print("\n\n=== PYQs 2024 FORMAT ===")
for i, line in enumerate(lines):
    if 'NEET-PG-PYQs-2024' in line:
        print(f'PYQs 2024 starts at line {i+1}')
        for j in range(i, min(i+80, len(lines))):
            print(f'{j+1}: {lines[j]}', end='')
        break
