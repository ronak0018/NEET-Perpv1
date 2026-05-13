import os
from PyPDF2 import PdfReader

files_dir = os.path.join(os.path.dirname(__file__), "Files")

for filename in sorted(os.listdir(files_dir)):
    if not filename.endswith(".pdf"):
        continue
    filepath = os.path.join(files_dir, filename)
    print(f"\n{'='*80}")
    print(f"FILE: {filename}")
    print(f"{'='*80}")
    try:
        reader = PdfReader(filepath)
        print(f"Pages: {len(reader.pages)}")
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                print(f"\n--- Page {i+1} ---")
                # Print first 2000 chars per page to keep output manageable
                print(text[:2000])
                if len(text) > 2000:
                    print(f"... [truncated, {len(text)} total chars]")
    except Exception as e:
        print(f"ERROR: {e}")
