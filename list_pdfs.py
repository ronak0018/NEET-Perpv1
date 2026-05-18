import re

with open('neet_pyq_extracted.txt', 'r', encoding='utf-8') as f:
    content = f.read()

files = re.findall(r'FILE: (.+?)\.pdf', content)
print(f"Total PDFs: {len(files)}")
for fn in files:
    print(f"  {fn}")
