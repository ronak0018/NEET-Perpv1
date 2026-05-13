"""Seed script to parse NEET PG questions from PDFs and populate MongoDB Atlas."""

import asyncio
import re
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load env from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# ---------------------------------------------------------------------------
# Parsers for the two NEET PG PDF text extractions
# ---------------------------------------------------------------------------

def parse_pyqs_2024(text: str) -> list[dict]:
    """Parse NEET PG PYQs 2024 format.
    The PDF extraction puts each word on a separate line, so we first join
    everything into a single string, then parse by Q.N. / options / Correct Answer.
    """
    # Pre-process: remove page markers, join fragmented words
    text = re.sub(r'---\s*Page\s+\d+\s*---', '', text)
    lines = [l.strip() for l in text.split('\n')
             if l.strip() and 'PrepLadder' not in l]
    joined = re.sub(r'\s+', ' ', ' '.join(lines)).strip()

    # Remove header text
    joined = re.sub(r'^.*?NEET\s+PG\s+PYQS\s+2024\s*', '', joined, flags=re.IGNORECASE)
    # Remove footer text
    joined = re.sub(r"Download\s+PrepLadder.*$", '', joined, flags=re.IGNORECASE)

    questions = []
    current_subject = None
    current_topic = ''

    SUBJECT_RE = re.compile(
        r'\b(Anesthesia|Anatomy|Biochemistry|Dermatology|ENT|'
        r'Forensic\s+Medicine(?:\s+and\s+Toxicology)?|'
        r'Microbiology|Ophthalmology|Orthopaedics|'
        r'Paediatrics|Pediatrics|Pathology|Pharmacology|'
        r'Physiology|Psychiatry|Radiology|PSM|SPM|'
        r'Community\s+Medicine|Medicine|Surgery|'
        r'Obstetrics(?:\s+and\s+Gynaecology)?|Gynaecology)\b',
        re.IGNORECASE
    )

    # Find all Q.N. positions and Correct Answer: positions
    q_iter = list(re.finditer(r'Q\.(\d+)\.\s*', joined))
    ca_iter = list(re.finditer(r'Correct\s+Answer:\s*', joined, re.IGNORECASE))

    for qi, qm in enumerate(q_iter):
        next_q_start = q_iter[qi + 1].start() if qi + 1 < len(q_iter) else len(joined)

        # Find Correct Answer: between this Q and next Q
        ca = None
        for cam in ca_iter:
            if qm.start() < cam.start() < next_q_start:
                ca = cam
                break
        if not ca:
            continue

        # Detect subject/topic from text before this Q (after previous Correct Answer)
        prev_ca_end = 0
        for cam in ca_iter:
            if cam.end() <= qm.start():
                prev_ca_end = cam.end()
        pre_text = joined[prev_ca_end:qm.start()]

        # Use LAST subject match in pre_text (most recent subject header)
        subj_matches = list(SUBJECT_RE.finditer(pre_text))
        if subj_matches:
            current_subject = normalize_subject(subj_matches[-1].group(0))

        topic_m = re.search(r'Topic:\s*(.*?)(?=Q\.\d+\.|$)', pre_text, re.IGNORECASE)
        if topic_m:
            current_topic = topic_m.group(1).strip()

        # Question + options text (between Q.N. end and Correct Answer: start)
        q_opts = joined[qm.end():ca.start()].strip()

        # Correct answer text (between CA end and next Q start)
        answer_rest = joined[ca.end():next_q_start].strip()
        # Trim subject/topic text from the answer
        correct_text = re.split(
            r'\s+(?=(?:Anesthesia|Anatomy|Biochemistry|Dermatology|ENT|'
            r'Forensic\s+Medicine|Microbiology|Ophthalmology|Orthopaedics|'
            r'Paediatrics|Pediatrics|Pathology|Pharmacology|Physiology|'
            r'Psychiatry|Radiology|PSM|SPM|Community\s+Medicine|'
            r'Medicine|Surgery|Obstetrics|Gynaecology|Topic:)\b)',
            answer_rest, flags=re.IGNORECASE
        )[0].strip()

        # Find numbered options 1. 2. 3. 4.
        opt_positions = list(re.finditer(r'\b([1-4])\.\s', q_opts))
        # Find first contiguous 1,2,3,4 set
        best_set = None
        for si in range(len(opt_positions) - 3):
            nums = [int(opt_positions[si + j].group(1)) for j in range(4)]
            if nums == [1, 2, 3, 4]:
                best_set = opt_positions[si:si + 4]
                break
        if not best_set:
            continue

        q_text = q_opts[:best_set[0].start()].strip()
        options = []
        for oi in range(4):
            opt_s = best_set[oi].end()
            opt_e = best_set[oi + 1].start() if oi + 1 < 4 else len(q_opts)
            options.append(q_opts[opt_s:opt_e].strip())

        if not q_text or len(options) != 4:
            continue

        correct_idx = find_correct_option(options, correct_text)

        questions.append({
            "subject": current_subject or "General",
            "topic": current_topic or "General",
            "question": clean_text(q_text),
            "options": [clean_text(o) for o in options],
            "correct_answer": correct_idx,
            "explanation": f"Correct answer: {correct_text}",
            "difficulty": "medium",
            "source": "NEET PG 2024 PYQs",
            "year": 2024,
        })

    return questions


# Subject header pattern for Recall 2025 (includes abbreviations found in PDF)
_RECALL_SUBJECT_RE = re.compile(
    r'^(Anatomy|Physiology|Biochemistry|Pathology|Pharmacology|'
    r'Microbiology|Forensic\s*Medicine|FMT|PSM|SPM|ENT|'
    r'Ophtha(?:lmology)?|Pedia(?:trics)?|Paediatrics|Pediatrics|'
    r'OBG|Obstetrics|Gynaecology|'
    r'Obs(?:tetrics)?\s*(?:and|&)\s*Gyn(?:aecology|ecology)?|'
    r'Medicine|Surgery|Radiology|Anaesthesia|Anesthesia|'
    r'Ortho(?:paedics)?|Psychiatry|Derma(?:tology)?|'
    r'Community\s*Medicine|Preventive\s*Medicine)$',
    re.IGNORECASE
)

# Question start pattern: Q. or Q1. or Q15. etc.
_Q_RE = re.compile(r'^Q\d*\.\s*(.*)')

# Option patterns
_OPT_ABCD_RE = re.compile(r'^([ABCD])\.\s*(.*)')
_OPT_NUM_RE = re.compile(r'^([1-4])\.\s*(.*)')


def parse_recall_2025(text: str) -> list[dict]:
    """Parse NEET PG Recall Questions 2025 format.
    Handles Q./Q1./Q2. starts, A/B/C/D and 1/2/3/4 option styles,
    and abbreviated subject headers (FMT, OBG, Ophtha, Pedia, etc.).
    """
    # Remove page markers
    text = re.sub(r'---\s*Page\s+\d+\s*---', '', text)
    lines = text.split('\n')

    questions = []
    current_subject = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip blanks and boilerplate
        if not line or line.startswith('NEETPG') or line.startswith('Pages:') or line == 'Recall Questions':
            i += 1
            continue

        # Check subject header
        if _RECALL_SUBJECT_RE.match(line):
            current_subject = normalize_subject(line)
            i += 1
            continue

        # Check question start
        qm = _Q_RE.match(line)
        if qm:
            q_text = qm.group(1).strip()
            i += 1

            # Collect question text until first option (A./B./C./D. or 1./2./3./4.)
            while i < len(lines):
                l = lines[i].strip()
                if not l or l.startswith('NEETPG') or l.startswith('Pages:'):
                    i += 1
                    continue
                if _OPT_ABCD_RE.match(l) or _OPT_NUM_RE.match(l):
                    break
                if _Q_RE.match(l) or _RECALL_SUBJECT_RE.match(l):
                    break  # Question with no options
                q_text += ' ' + l
                i += 1

            # Detect option format
            if i >= len(lines):
                continue
            l = lines[i].strip()
            if _OPT_ABCD_RE.match(l):
                opt_labels = ['A', 'B', 'C', 'D']
            elif _OPT_NUM_RE.match(l):
                opt_labels = ['1', '2', '3', '4']
            else:
                continue  # No options found, skip

            # Collect 4 options
            options = []
            for idx, label in enumerate(opt_labels):
                next_label = opt_labels[idx + 1] if idx < 3 else None
                opt_text = ''

                if i < len(lines):
                    l = lines[i].strip()
                    om = re.match(rf'^{re.escape(label)}\.\s*(.*)', l)
                    if om:
                        opt_text = om.group(1).strip()
                        i += 1
                        while i < len(lines):
                            nl = lines[i].strip()
                            if not nl:
                                i += 1
                                continue
                            if nl.startswith('NEETPG') or nl.startswith('Pages:'):
                                i += 1
                                continue
                            # Break for next option
                            if next_label and re.match(rf'^{re.escape(next_label)}\.\s', nl):
                                break
                            # Break for last option (D or 4)
                            if not next_label:
                                if (_Q_RE.match(nl) or _RECALL_SUBJECT_RE.match(nl)
                                        or _OPT_ABCD_RE.match(nl) or re.match(r'^1\.\s', nl)):
                                    break
                            opt_text += ' ' + nl
                            i += 1
                    else:
                        options.append(f'Option {label}')
                        continue

                options.append(clean_text(opt_text) if opt_text.strip() else f'Option {label}')

            if (q_text.strip() and len(options) == 4
                    and any(o != f'Option {l}' for o, l in zip(options, opt_labels))):
                questions.append({
                    "subject": current_subject or "General",
                    "topic": "General",
                    "question": clean_text(q_text),
                    "options": options,
                    "correct_answer": 0,
                    "explanation": "NEET PG 2025 Recall Question",
                    "difficulty": "medium",
                    "source": "NEET PG 2025 Recall",
                    "year": 2025,
                })
            continue
        i += 1

    return questions


def normalize_subject(s: str) -> str:
    """Normalize subject names to consistent format."""
    s = s.strip()
    mapping = {
        "anesthesia": "Anaesthesia",
        "anaesthesia": "Anaesthesia",
        "derma": "Dermatology",
        "dermatology": "Dermatology",
        "ent": "ENT",
        "fmt": "Forensic Medicine",
        "forensic medicine": "Forensic Medicine",
        "forensic medicine and toxicology": "Forensic Medicine",
        "general medicine": "Medicine",
        "general surgery": "Surgery",
        "gynaecology": "Obstetrics & Gynaecology",
        "obstetrics": "Obstetrics & Gynaecology",
        "obstetrics and gynaecology": "Obstetrics & Gynaecology",
        "obstetrics & gynaecology": "Obstetrics & Gynaecology",
        "obg": "Obstetrics & Gynaecology",
        "obs and gyn": "Obstetrics & Gynaecology",
        "ophtha": "Ophthalmology",
        "ophthalmology": "Ophthalmology",
        "ortho": "Orthopaedics",
        "orthopaedics": "Orthopaedics",
        "pedia": "Paediatrics",
        "paediatrics": "Paediatrics",
        "pediatrics": "Paediatrics",
        "psm": "PSM",
        "spm": "PSM",
        "community medicine": "PSM",
        "social and preventive medicine": "PSM",
        "preventive medicine": "PSM",
    }
    return mapping.get(s.lower(), s.title())


def clean_text(text: str) -> str:
    """Clean extracted text."""
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s*\n\s*', ' ', text)
    return text


def find_correct_option(options: list[str], correct_text: str) -> int:
    """Find which option index matches the correct answer text."""
    correct_lower = correct_text.lower().strip()
    
    # Try exact match first
    for i, opt in enumerate(options):
        if opt.lower().strip() == correct_lower:
            return i
    
    # Try substring match
    for i, opt in enumerate(options):
        if correct_lower in opt.lower() or opt.lower() in correct_lower:
            return i
    
    # Try word overlap
    correct_words = set(correct_lower.split())
    best_idx = 0
    best_score = 0
    for i, opt in enumerate(options):
        opt_words = set(opt.lower().split())
        overlap = len(correct_words & opt_words)
        if overlap > best_score:
            best_score = overlap
            best_idx = i
    
    return best_idx if best_score > 0 else 0


# ---------------------------------------------------------------------------
# Syllabus-based notes
# ---------------------------------------------------------------------------

SYLLABUS_NOTES = [
    {
        "subject": "Anatomy",
        "topic": "Brachial Plexus",
        "title": "Brachial Plexus - High Yield Notes",
        "content": """# Brachial Plexus\n\n## Roots: C5, C6, C7, C8, T1\n\n## Trunks\n- **Upper trunk**: C5 + C6\n- **Middle trunk**: C7\n- **Lower trunk**: C8 + T1\n\n## Important Nerve Injuries\n| Nerve | Injury | Deficit |\n|-------|--------|---------|\n| Long thoracic | Mastectomy | Winging of scapula |\n| Axillary | Surgical neck fracture | Loss of shoulder abduction |\n| Radial | Midshaft humerus fracture | Wrist drop |\n| Median | Supracondylar fracture | Hand of benediction |\n| Ulnar | Medial epicondyle fracture | Claw hand |\n\n## Erb-Duchenne Palsy (C5-C6)\n- Waiter's tip position\n- Loss of abduction, lateral rotation, flexion at elbow\n\n## Klumpke's Palsy (C8-T1)\n- Total claw hand\n- Loss of intrinsic muscles\n- Horner's syndrome if T1 involved""",
    },
    {
        "subject": "Physiology",
        "topic": "Cardiovascular System",
        "title": "Cardiac Cycle - Quick Revision",
        "content": """# Cardiac Cycle\n\n## Phases\n1. **Atrial systole** - Atrial contraction, 'a' wave in JVP\n2. **Isovolumetric contraction** - All valves closed, highest O2 consumption\n3. **Rapid ejection** - Aortic valve opens\n4. **Reduced ejection**\n5. **Isovolumetric relaxation** - All valves closed again\n6. **Rapid filling** - S3 heard here\n7. **Reduced filling (diastasis)**\n\n## Heart Sounds\n- **S1**: Closure of AV valves\n- **S2**: Closure of semilunar valves\n- **S3**: Rapid ventricular filling\n- **S4**: Atrial kick against stiff ventricle\n\n## Key Values\n- Cardiac Output = SV x HR = 5 L/min\n- Stroke Volume = EDV - ESV = 70 ml\n- Ejection Fraction = SV/EDV = ~60%""",
    },
    {
        "subject": "Pharmacology",
        "topic": "Autonomic Nervous System",
        "title": "Cholinergic & Anticholinergic Drugs",
        "content": """# Autonomic Pharmacology\n\n## Direct Acting Cholinergics\n- **Muscarinic**: Pilocarpine, Methacholine, Bethanechol\n- **Nicotinic**: Succinylcholine\n\n## Indirect Acting (Anticholinesterases)\n- **Reversible**: Physostigmine, Neostigmine, Edrophonium\n- **Irreversible**: Organophosphates\n\n## Anticholinergic Drugs\n- Atropine, Ipratropium, Glycopyrrolate, Oxybutynin\n\n## Atropine Poisoning\n- Hot as a hare, Dry as a bone, Red as a beet, Blind as a bat, Mad as a hatter\n\n## OP Poisoning Treatment\n- Atropine + Pralidoxime (2-PAM)""",
    },
    {
        "subject": "Pathology",
        "topic": "Neoplasia",
        "title": "Tumor Markers - Complete List",
        "content": """# Tumor Markers\n\n| Marker | Cancer |\n|--------|--------|\n| AFP | HCC, Yolk sac tumor |\n| CEA | Colorectal, Pancreatic |\n| CA-125 | Ovarian |\n| CA 19-9 | Pancreatic |\n| CA 15-3 | Breast |\n| PSA | Prostate |\n| HCG | Choriocarcinoma |\n| Calcitonin | Medullary thyroid |\n| S-100 | Melanoma, Schwannoma |\n| LDH | Lymphoma |\n| ALP | Bone metastasis, Paget's |""",
    },
    {
        "subject": "Microbiology",
        "topic": "Bacteriology",
        "title": "Gram Staining & Bacterial Classification",
        "content": """# Bacterial Classification\n\n## Gram Positive Cocci\n- **Staphylococcus**: Clusters, catalase +ve (S. aureus: coagulase +ve)\n- **Streptococcus**: Chains, catalase -ve (S. pyogenes: Group A)\n\n## Gram Negative Cocci\n- Neisseria meningitidis, N. gonorrhoeae\n\n## Gram Positive Bacilli\n- Clostridium (anaerobic), Bacillus (aerobic), Corynebacterium\n\n## Gram Negative Bacilli\n- E. coli, Klebsiella, Pseudomonas, Salmonella\n\n## Acid-Fast Bacilli\n- M. tuberculosis (ZN stain), M. leprae (Modified ZN)""",
    },
    {
        "subject": "Medicine",
        "topic": "Cardiology",
        "title": "ECG Interpretation - Quick Guide",
        "content": """# ECG Interpretation\n\n## Normal Values\n- Rate: 60-100 bpm\n- PR interval: 0.12-0.20s\n- QRS duration: <0.12s\n- QT interval: <0.44s\n\n## ST Elevation MI\n- Anterior: V1-V4 (LAD)\n- Inferior: II, III, aVF (RCA)\n- Lateral: I, aVL, V5-V6 (LCx)\n\n## Arrhythmias\n- AF: Irregularly irregular, no P waves\n- SVT: Narrow complex tachycardia\n- VT: Wide complex tachycardia\n- VF: Chaotic, no organized QRS""",
    },
    {
        "subject": "Surgery",
        "topic": "General Surgery",
        "title": "Thyroid Surgery - Key Points",
        "content": """# Thyroid Surgery\n\n## Indications\n- Malignancy, compressive symptoms, cosmetic, toxic goitre\n\n## Nerves at Risk\n- **RLN**: Voice change (most feared complication)\n- **External laryngeal nerve**: Loss of high-pitched voice\n\n## Complications\n- Hemorrhage, hypocalcemia (parathyroid damage)\n- Thyroid storm, wound infection\n\n## Thyroid Cancers\n- Papillary (70-80%): Best prognosis, lymphatic spread\n- Follicular (10-15%): Hematogenous spread\n- Medullary (5-10%): Calcitonin marker, MEN 2\n- Anaplastic (1-2%): Worst prognosis""",
    },
    {
        "subject": "Obstetrics & Gynaecology",
        "topic": "High Risk Pregnancy",
        "title": "Preeclampsia & Eclampsia",
        "content": """# Preeclampsia & Eclampsia\n\n## Preeclampsia\n- BP ≥140/90 after 20 weeks + proteinuria\n- Severe: BP ≥160/110, proteinuria >5g/24hr\n\n## Treatment\n- **Antihypertensive**: Labetalol, Nifedipine, Methyldopa\n- **Seizure prophylaxis**: MgSO4 (Pritchard/Zuspan regimen)\n- **Definitive**: Delivery\n\n## MgSO4 Toxicity Monitoring\n- Knee jerk reflex (first to disappear)\n- Respiratory rate (>16/min)\n- Urine output (>25 ml/hr)\n- Antidote: Calcium gluconate""",
    },
]

# ---------------------------------------------------------------------------
# NEET PG Syllabus metadata
# ---------------------------------------------------------------------------

NEETPG_SUBJECTS = {
    "Anatomy": {"phase": "Phase I - Pre-clinical", "questions": 17},
    "Physiology": {"phase": "Phase I - Pre-clinical", "questions": 17},
    "Biochemistry": {"phase": "Phase I - Pre-clinical", "questions": 16},
    "Pathology": {"phase": "Phase II - Para-clinical", "questions": 25},
    "Pharmacology": {"phase": "Phase II - Para-clinical", "questions": 20},
    "Microbiology": {"phase": "Phase II - Para-clinical", "questions": 20},
    "Forensic Medicine": {"phase": "Phase II - Para-clinical", "questions": 10},
    "PSM": {"phase": "Phase II - Para-clinical", "questions": 25},
    "Medicine": {"phase": "Phase III - Clinical", "questions": 30},
    "Surgery": {"phase": "Phase III - Clinical", "questions": 30},
    "Obstetrics & Gynaecology": {"phase": "Phase III - Clinical", "questions": 20},
    "Paediatrics": {"phase": "Phase III - Clinical", "questions": 10},
    "ENT": {"phase": "Phase III - Clinical", "questions": 10},
    "Ophthalmology": {"phase": "Phase III - Clinical", "questions": 10},
    "Anaesthesia": {"phase": "Phase III - Clinical", "questions": 5},
    "Radiology": {"phase": "Phase III - Clinical", "questions": 5},
    "Dermatology": {"phase": "Phase III - Clinical", "questions": 5},
    "Orthopaedics": {"phase": "Phase III - Clinical", "questions": 10},
    "Psychiatry": {"phase": "Phase III - Clinical", "questions": 5},
}


async def seed():
    print(f"Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    # Test connection
    try:
        await client.admin.command("ping")
        print("Connected to MongoDB Atlas successfully!")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # ── Parse questions from PDFs ──
    pdf_text_path = os.path.join(os.path.dirname(__file__), "pdf_extracted.txt")
    if not os.path.exists(pdf_text_path):
        print("ERROR: pdf_extracted.txt not found. Run extract_pdfs2.py first.")
        sys.exit(1)

    with open(pdf_text_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Split by FILE markers
    file_sections = re.split(r'={80}\nFILE: .+\n={80}', full_text)
    file_names = re.findall(r'={80}\nFILE: (.+)\n={80}', full_text)

    all_questions = []

    for name, section in zip(file_names, file_sections[1:]):
        if "PYQs-2024" in name:
            print(f"\nParsing: {name}")
            qs = parse_pyqs_2024(section)
            print(f"  Found {len(qs)} questions")
            all_questions.extend(qs)
        elif "Recall-Questions-2025" in name:
            print(f"\nParsing: {name}")
            qs = parse_recall_2025(section)
            print(f"  Found {len(qs)} questions")
            all_questions.extend(qs)

    print(f"\nTotal questions parsed from PDFs: {len(all_questions)}")

    # ── Print subject distribution ──
    subjects = {}
    for q in all_questions:
        subjects[q["subject"]] = subjects.get(q["subject"], 0) + 1
    print("\nSubject distribution:")
    for s, c in sorted(subjects.items()):
        print(f"  {s}: {c} questions")

    # ── Clear and seed ──
    await db.questions.delete_many({})
    await db.notes.delete_many({})
    await db.subjects.delete_many({})
    print("\nCleared existing collections.")

    # Insert questions
    now = datetime.now(timezone.utc)
    for q in all_questions:
        q["created_at"] = now

    if all_questions:
        await db.questions.insert_many(all_questions)
        print(f"Inserted {len(all_questions)} questions")

    # Insert notes
    for n in SYLLABUS_NOTES:
        n["created_at"] = now
        n["updated_at"] = now
    await db.notes.insert_many(SYLLABUS_NOTES)
    print(f"Inserted {len(SYLLABUS_NOTES)} notes")

    # Insert subject metadata
    subject_docs = []
    for name, info in NEETPG_SUBJECTS.items():
        q_count = subjects.get(name, 0)
        subject_docs.append({
            "name": name,
            "phase": info["phase"],
            "exam_questions": info["questions"],
            "available_questions": q_count,
            "created_at": now,
        })
    await db.subjects.insert_many(subject_docs)
    print(f"Inserted {len(subject_docs)} subject records")

    # ── Create indexes ──
    await db.questions.create_index("subject")
    await db.questions.create_index("topic")
    await db.questions.create_index("difficulty")
    await db.questions.create_index("source")
    await db.questions.create_index("year")
    await db.notes.create_index("subject")
    await db.notes.create_index([("title", "text"), ("content", "text")])
    await db.subjects.create_index("name", unique=True)
    print("Created indexes.")

    print("\n✓ Seed completed successfully!")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
