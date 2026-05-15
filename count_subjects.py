import json, os

folder = "Files/questions"
subjects = set()
chapters = set()

for f in os.listdir(folder):
    if f.endswith(".json"):
        with open(os.path.join(folder, f), encoding="utf-8") as fp:
            data = json.load(fp)
        questions = data.get("questions", data) if isinstance(data, dict) else data
        for q in questions:
            subj = q.get("subject")
            topic = q.get("topic")
            subjects.add(subj)
            chapters.add((subj, topic))

print(f"Total Subjects: {len(subjects)}")
print(f"Total Chapters (unique subject+topic): {len(chapters)}")
print()
print("=== Subjects ===")
for s in sorted(subjects, key=lambda x: str(x)):
    topics = sorted(set(t for (sb, t) in chapters if sb == s), key=lambda x: str(x))
    print(f"\n{s} ({len(topics)} chapters):")
    for t in topics:
        print(f"  - {t}")
