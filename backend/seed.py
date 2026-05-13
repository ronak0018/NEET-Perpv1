"""Seed script to populate MongoDB with sample NEET PG questions and notes."""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "neetpg")

SAMPLE_QUESTIONS = [
    {
        "subject": "Anatomy",
        "topic": "Upper Limb",
        "question": "Which nerve is most commonly injured in fracture of the surgical neck of the humerus?",
        "options": ["Radial nerve", "Axillary nerve", "Ulnar nerve", "Median nerve"],
        "correct_answer": 1,
        "explanation": "The axillary nerve wraps around the surgical neck of the humerus and is most vulnerable to injury in fractures at this site.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Upper Limb",
        "question": "Erb's point is located at which vertebra level?",
        "options": ["C4", "C5", "C6", "C7"],
        "correct_answer": 2,
        "explanation": "Erb's point is the junction of C5 and C6 nerve roots forming the upper trunk of the brachial plexus at the C6 vertebral level.",
        "difficulty": "medium",
    },
    {
        "subject": "Anatomy",
        "topic": "Lower Limb",
        "question": "The femoral nerve arises from which lumbar plexus roots?",
        "options": ["L1, L2", "L2, L3, L4", "L3, L4, L5", "L4, L5, S1"],
        "correct_answer": 1,
        "explanation": "The femoral nerve is the largest branch of the lumbar plexus, arising from the posterior divisions of L2, L3, and L4.",
        "difficulty": "easy",
    },
    {
        "subject": "Physiology",
        "topic": "Cardiovascular System",
        "question": "The normal cardiac output in a resting adult is approximately?",
        "options": ["3 L/min", "5 L/min", "7 L/min", "10 L/min"],
        "correct_answer": 1,
        "explanation": "Normal cardiac output at rest is approximately 5 L/min (stroke volume ~70 ml x heart rate ~72 bpm).",
        "difficulty": "easy",
    },
    {
        "subject": "Physiology",
        "topic": "Cardiovascular System",
        "question": "Which phase of the cardiac cycle has the highest oxygen consumption?",
        "options": [
            "Isovolumetric contraction",
            "Rapid ejection",
            "Isovolumetric relaxation",
            "Rapid filling",
        ],
        "correct_answer": 0,
        "explanation": "Isovolumetric contraction phase has the highest myocardial oxygen consumption as the ventricle generates maximum wall tension.",
        "difficulty": "hard",
    },
    {
        "subject": "Physiology",
        "topic": "Renal Physiology",
        "question": "The normal GFR in a healthy adult is approximately?",
        "options": ["60 ml/min", "90 ml/min", "125 ml/min", "180 ml/min"],
        "correct_answer": 2,
        "explanation": "Normal GFR is approximately 125 ml/min or 180 L/day. This is the rate at which plasma is filtered through the glomeruli.",
        "difficulty": "easy",
    },
    {
        "subject": "Biochemistry",
        "topic": "Enzymes",
        "question": "Which enzyme is deficient in Phenylketonuria (PKU)?",
        "options": [
            "Tyrosinase",
            "Phenylalanine hydroxylase",
            "Homogentisic acid oxidase",
            "Cystathionine synthase",
        ],
        "correct_answer": 1,
        "explanation": "PKU is caused by deficiency of phenylalanine hydroxylase, which converts phenylalanine to tyrosine.",
        "difficulty": "easy",
    },
    {
        "subject": "Biochemistry",
        "topic": "Vitamins",
        "question": "Wernicke's encephalopathy is caused by deficiency of which vitamin?",
        "options": ["Vitamin B12", "Vitamin B1 (Thiamine)", "Vitamin B6", "Niacin"],
        "correct_answer": 1,
        "explanation": "Wernicke's encephalopathy is caused by thiamine (Vitamin B1) deficiency, commonly seen in chronic alcoholism.",
        "difficulty": "medium",
    },
    {
        "subject": "Pharmacology",
        "topic": "Autonomic Nervous System",
        "question": "Atropine acts by blocking which receptor?",
        "options": ["Nicotinic", "Muscarinic", "Alpha adrenergic", "Beta adrenergic"],
        "correct_answer": 1,
        "explanation": "Atropine is a competitive antagonist at muscarinic acetylcholine receptors (M1-M5).",
        "difficulty": "easy",
    },
    {
        "subject": "Pharmacology",
        "topic": "Antibiotics",
        "question": "Which antibiotic acts by inhibiting cell wall synthesis?",
        "options": ["Tetracycline", "Penicillin", "Erythromycin", "Ciprofloxacin"],
        "correct_answer": 1,
        "explanation": "Penicillin inhibits bacterial cell wall synthesis by binding to penicillin-binding proteins (PBPs) and preventing transpeptidation.",
        "difficulty": "easy",
    },
    {
        "subject": "Pathology",
        "topic": "Neoplasia",
        "question": "Which tumor marker is associated with hepatocellular carcinoma?",
        "options": ["CEA", "AFP", "CA-125", "PSA"],
        "correct_answer": 1,
        "explanation": "Alpha-fetoprotein (AFP) is the most important tumor marker for hepatocellular carcinoma. Elevated levels are also seen in yolk sac tumors.",
        "difficulty": "easy",
    },
    {
        "subject": "Pathology",
        "topic": "Hematology",
        "question": "Reed-Sternberg cells are pathognomonic of which disease?",
        "options": [
            "Non-Hodgkin lymphoma",
            "Hodgkin lymphoma",
            "Multiple myeloma",
            "Chronic lymphocytic leukemia",
        ],
        "correct_answer": 1,
        "explanation": "Reed-Sternberg cells (large binucleated cells with 'owl-eye' appearance) are the hallmark of Hodgkin lymphoma.",
        "difficulty": "easy",
    },
    {
        "subject": "Microbiology",
        "topic": "Bacteriology",
        "question": "Which organism causes gas gangrene?",
        "options": [
            "Clostridium tetani",
            "Clostridium perfringens",
            "Clostridium botulinum",
            "Clostridium difficile",
        ],
        "correct_answer": 1,
        "explanation": "Clostridium perfringens (formerly C. welchii) is the most common cause of gas gangrene (clostridial myonecrosis).",
        "difficulty": "easy",
    },
    {
        "subject": "Microbiology",
        "topic": "Virology",
        "question": "Which hepatitis virus is a DNA virus?",
        "options": [
            "Hepatitis A",
            "Hepatitis B",
            "Hepatitis C",
            "Hepatitis E",
        ],
        "correct_answer": 1,
        "explanation": "Hepatitis B is the only DNA virus among the hepatitis viruses. It belongs to the Hepadnaviridae family.",
        "difficulty": "medium",
    },
    {
        "subject": "Surgery",
        "topic": "General Surgery",
        "question": "Most common type of thyroid carcinoma is?",
        "options": ["Follicular", "Papillary", "Medullary", "Anaplastic"],
        "correct_answer": 1,
        "explanation": "Papillary carcinoma accounts for 70-80% of all thyroid cancers. It has the best prognosis and spreads via lymphatics.",
        "difficulty": "easy",
    },
    {
        "subject": "Medicine",
        "topic": "Cardiology",
        "question": "The most common cause of mitral stenosis is?",
        "options": [
            "Congenital",
            "Rheumatic heart disease",
            "Infective endocarditis",
            "Carcinoid syndrome",
        ],
        "correct_answer": 1,
        "explanation": "Rheumatic heart disease is the most common cause of mitral stenosis, accounting for >95% of cases in developing countries.",
        "difficulty": "easy",
    },
    {
        "subject": "Medicine",
        "topic": "Endocrinology",
        "question": "Conn's syndrome is caused by excess of?",
        "options": ["Cortisol", "Aldosterone", "Adrenaline", "Thyroxine"],
        "correct_answer": 1,
        "explanation": "Conn's syndrome (primary hyperaldosteronism) is caused by excess aldosterone production, usually from an adrenal adenoma.",
        "difficulty": "medium",
    },
    {
        "subject": "Obstetrics",
        "topic": "Normal Pregnancy",
        "question": "The most common presentation at term is?",
        "options": ["Breech", "Vertex", "Transverse", "Face"],
        "correct_answer": 1,
        "explanation": "Vertex (cephalic) presentation occurs in approximately 96% of term pregnancies.",
        "difficulty": "easy",
    },
    {
        "subject": "Pediatrics",
        "topic": "Neonatology",
        "question": "The most common cause of neonatal sepsis in India is?",
        "options": [
            "E. coli",
            "Klebsiella",
            "Group B Streptococcus",
            "Staphylococcus aureus",
        ],
        "correct_answer": 1,
        "explanation": "Klebsiella is the most common cause of neonatal sepsis in India, while Group B Streptococcus is most common in Western countries.",
        "difficulty": "medium",
    },
    {
        "subject": "Ophthalmology",
        "topic": "Glaucoma",
        "question": "The most common type of glaucoma is?",
        "options": [
            "Angle closure",
            "Primary open angle",
            "Congenital",
            "Secondary",
        ],
        "correct_answer": 1,
        "explanation": "Primary open angle glaucoma (POAG) is the most common type, accounting for ~60-70% of all glaucoma cases worldwide.",
        "difficulty": "easy",
    },
]

SAMPLE_NOTES = [
    {
        "subject": "Anatomy",
        "topic": "Brachial Plexus",
        "title": "Brachial Plexus - High Yield Notes",
        "content": """# Brachial Plexus

## Roots: C5, C6, C7, C8, T1

## Trunks
- **Upper trunk**: C5 + C6
- **Middle trunk**: C7
- **Lower trunk**: C8 + T1

## Important Nerve Injuries
| Nerve | Injury | Deficit |
|-------|--------|---------|
| Long thoracic | Mastectomy | Winging of scapula |
| Axillary | Surgical neck fracture | Loss of shoulder abduction |
| Radial | Midshaft humerus fracture | Wrist drop |
| Median | Supracondylar fracture | Hand of benediction |
| Ulnar | Medial epicondyle fracture | Claw hand |

## Erb-Duchenne Palsy (C5-C6)
- Waiter's tip position
- Loss of abduction, lateral rotation, flexion at elbow

## Klumpke's Palsy (C8-T1)
- Total claw hand
- Loss of intrinsic muscles
- Horner's syndrome if T1 involved
""",
    },
    {
        "subject": "Physiology",
        "topic": "Cardiovascular System",
        "title": "Cardiac Cycle - Quick Revision",
        "content": """# Cardiac Cycle

## Phases
1. **Atrial systole** - Atrial contraction, 'a' wave in JVP
2. **Isovolumetric contraction** - All valves closed, highest O2 consumption
3. **Rapid ejection** - Aortic valve opens
4. **Reduced ejection**
5. **Isovolumetric relaxation** - All valves closed again
6. **Rapid filling** - S3 heard here (pathological in adults)
7. **Reduced filling (diastasis)**

## Heart Sounds
- **S1**: Closure of AV valves (mitral + tricuspid)
- **S2**: Closure of semilunar valves (aortic + pulmonary)
- **S3**: Rapid ventricular filling (normal in young)
- **S4**: Atrial kick against stiff ventricle

## Key Values
- Cardiac Output = SV x HR = 5 L/min
- Stroke Volume = EDV - ESV = 70 ml
- Ejection Fraction = SV/EDV = ~60%
""",
    },
    {
        "subject": "Pharmacology",
        "topic": "Autonomic Nervous System",
        "title": "Cholinergic & Anticholinergic Drugs",
        "content": """# Autonomic Pharmacology

## Cholinergic Drugs (Parasympathomimetics)

### Direct Acting
- **Muscarinic**: Pilocarpine, Methacholine, Bethanechol
- **Nicotinic**: Succinylcholine

### Indirect Acting (Anticholinesterases)
- **Reversible**: Physostigmine, Neostigmine, Edrophonium
- **Irreversible**: Organophosphates (Malathion, Parathion)

## Anticholinergic Drugs
- **Atropine**: Mydriasis, tachycardia, dry mouth
- **Ipratropium**: Bronchodilator (inhaled)
- **Glycopyrrolate**: Pre-anesthetic medication
- **Oxybutynin**: Overactive bladder

## Atropine Poisoning Mnemonics
- **Hot** as a hare (hyperthermia)
- **Dry** as a bone (no secretions)
- **Red** as a beet (vasodilation)
- **Blind** as a bat (mydriasis)
- **Mad** as a hatter (delirium)

## Treatment of OP Poisoning
- **Atropine** (muscarinic antagonist)
- **Pralidoxime (2-PAM)** - reactivates AChE if given within 24-48 hours
""",
    },
    {
        "subject": "Pathology",
        "topic": "Neoplasia",
        "title": "Tumor Markers - Complete List",
        "content": """# Tumor Markers

| Marker | Associated Cancer |
|--------|------------------|
| AFP | Hepatocellular carcinoma, Yolk sac tumor |
| CEA | Colorectal, Pancreatic, Lung |
| CA-125 | Ovarian cancer |
| CA 19-9 | Pancreatic cancer |
| CA 15-3 | Breast cancer |
| PSA | Prostate cancer |
| HCG | Choriocarcinoma, Testicular tumors |
| Calcitonin | Medullary thyroid carcinoma |
| Thyroglobulin | Follicular thyroid carcinoma |
| S-100 | Melanoma, Schwannoma |
| Acid phosphatase | Prostate (old marker) |
| LDH | Lymphoma, Seminoma |
| ALP | Bone metastasis, Paget's disease |

## Important Points
- PSA is organ-specific but NOT cancer-specific
- AFP + HCG both elevated = Mixed germ cell tumor
- CA-125 can be elevated in endometriosis
""",
    },
    {
        "subject": "Microbiology",
        "topic": "Bacteriology",
        "title": "Gram Staining & Bacterial Classification",
        "content": """# Bacterial Classification

## Gram Positive Cocci
- **Staphylococcus**: Clusters, catalase +ve
  - S. aureus: Coagulase +ve
  - S. epidermidis: Prosthetic infections
- **Streptococcus**: Chains, catalase -ve
  - S. pyogenes: Group A, beta hemolytic
  - S. pneumoniae: Alpha hemolytic, optochin sensitive

## Gram Negative Cocci
- **Neisseria meningitidis**: Meningitis
- **Neisseria gonorrhoeae**: STI

## Gram Positive Bacilli
- **Clostridium**: Anaerobic, spore-forming
- **Bacillus**: Aerobic, spore-forming
- **Corynebacterium**: Club-shaped

## Gram Negative Bacilli
- **E. coli**: UTI, neonatal meningitis
- **Klebsiella**: Pneumonia (currant jelly sputum)
- **Pseudomonas**: Blue-green pus
- **Salmonella**: Typhoid fever

## Acid-Fast Bacilli
- **M. tuberculosis**: ZN stain positive
- **M. leprae**: Modified ZN stain
""",
    },
]


async def seed():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    # Clear existing data
    await db.questions.delete_many({})
    await db.notes.delete_many({})

    # Insert questions
    now = datetime.utcnow()
    for q in SAMPLE_QUESTIONS:
        q["created_at"] = now
    await db.questions.insert_many(SAMPLE_QUESTIONS)
    print(f"Inserted {len(SAMPLE_QUESTIONS)} questions")

    # Insert notes
    for n in SAMPLE_NOTES:
        n["created_at"] = now
        n["updated_at"] = now
    await db.notes.insert_many(SAMPLE_NOTES)
    print(f"Inserted {len(SAMPLE_NOTES)} notes")

    # Create indexes
    await db.questions.create_index("subject")
    await db.questions.create_index("topic")
    await db.questions.create_index("difficulty")
    await db.notes.create_index("subject")
    await db.notes.create_index([("title", "text"), ("content", "text")])

    print("Seed completed successfully!")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
