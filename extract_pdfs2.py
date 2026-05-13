import os
from PyPDF2 import PdfReader

files_dir = os.path.join(os.path.dirname(__file__), "Files")
output_file = os.path.join(os.path.dirname(__file__), "pdf_extracted.txt")

with open(output_file, "w", encoding="utf-8") as out:
    for filename in sorted(os.listdir(files_dir)):
        if not filename.endswith(".pdf"):
            continue
        filepath = os.path.join(files_dir, filename)
        out.write(f"\n{'='*80}\n")
        out.write(f"FILE: {filename}\n")
        out.write(f"{'='*80}\n")
        try:
            reader = PdfReader(filepath)
            out.write(f"Pages: {len(reader.pages)}\n")
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    out.write(f"\n--- Page {i+1} ---\n")
                    out.write(text + "\n")
        except Exception as e:
            out.write(f"ERROR: {e}\n")

print(f"Extraction complete. Output saved to {output_file}")
# Print file size
size = os.path.getsize(output_file)
print(f"Output file size: {size} bytes ({size//1024} KB)")
