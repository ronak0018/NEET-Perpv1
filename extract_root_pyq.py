import pdfplumber
import os

os.chdir(r"c:\Ronak-EY\Non-GIT\Neet-PG")
base_dir = r"Files\NEET-PYQ"

output_file = "neet_pyq_root_extracted.txt"

# Only root-level PDFs - no subfolders
pdfs = sorted([f for f in os.listdir(base_dir) if f.endswith(".pdf")])
print(f"Found {len(pdfs)} root-level PDFs")

with open(output_file, "w", encoding="utf-8") as out:
    for filename in pdfs:
        filepath = os.path.join(base_dir, filename)
        out.write(f"\n{'='*80}\n")
        out.write(f"FILE: {filename}\n")
        out.write(f"{'='*80}\n")
        try:
            with pdfplumber.open(filepath) as pdf:
                for i, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text()
                        if text and text.strip():
                            out.write(f"\n--- Page {i+1} ---\n")
                            out.write(text + "\n")
                    except Exception as pe:
                        out.write(f"\n--- Page {i+1} ERROR: {pe} ---\n")
        except Exception as e:
            out.write(f"FILE ERROR: {e}\n")
        print(f"Done: {filename}", flush=True)

print(f"\nAll done! Output: {output_file}")
