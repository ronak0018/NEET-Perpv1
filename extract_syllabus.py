import pdfplumber
import os
import sys

os.chdir(r"c:\Ronak-EY\Non-GIT\Neet-PG")
base_dir = r"Files\NEET-PYQ"

output_file = "neet_pyq_extracted.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for root, dirs, files in os.walk(base_dir):
        # Skip Syllabus folder (already processed)
        if "Syllabus" in root:
            continue
        for filename in sorted(files):
            if not filename.endswith(".pdf"):
                continue
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, base_dir)
            f.write(f"\n{'='*80}\n")
            f.write(f"FILE: {rel_path}\n")
            f.write(f"{'='*80}\n")
            try:
                with pdfplumber.open(filepath) as pdf:
                    for i, page in enumerate(pdf.pages):
                        try:
                            text = page.extract_text()
                            if text and text.strip():
                                f.write(f"\n--- Page {i+1} ---\n")
                                f.write(text + "\n")
                        except Exception as pe:
                            f.write(f"\n--- Page {i+1} ERROR: {pe} ---\n")
            except Exception as e:
                f.write(f"FILE ERROR: {e}\n")
            print(f"Done: {rel_path}", flush=True)

print(f"\nAll done! Output saved to {output_file}")
