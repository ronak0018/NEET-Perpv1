"""
Seed Anatomy notes and MCQs from Complete_Anatomy_NEETPG_Notes.txt into MongoDB.
"""
import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).resolve().parent / "backend" / ".env")

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "neetpg")

# ─── NOTES (chapter-wise) ───────────────────────────────────────────────────

ANATOMY_NOTES = [
    {
        "subject": "Anatomy",
        "topic": "Upper Limb",
        "title": "Upper Limb – Rapid Revision",
        "content": """**Brachial Plexus:**
Roots → C5-T1

**Branches:**
- Musculocutaneous
- Axillary
- Radial
- Median
- Ulnar

**Erb's Palsy:**
- C5-C6 injury
- Waiter's tip deformity

**Klumpke's Palsy:**
- C8-T1 injury
- Claw hand

**Rotator Cuff Muscles (SITS):**
- Supraspinatus
- Infraspinatus
- Teres minor
- Subscapularis

**Carpal Tunnel Contents:**
- Median nerve
- Flexor tendons""",
    },
    {
        "subject": "Anatomy",
        "topic": "Lower Limb",
        "title": "Lower Limb – Rapid Revision",
        "content": """**Sciatic Nerve:**
Largest nerve in body.

**Femoral Triangle Boundaries:**
- Inguinal ligament
- Sartorius
- Adductor longus

**Contents (NAVEL):**
- Nerve
- Artery
- Vein
- Empty space
- Lymphatics

**Hip Joint:**
Blood supply → Medial circumflex femoral artery

**Foot Drop:**
Common peroneal nerve injury""",
    },
    {
        "subject": "Anatomy",
        "topic": "Thorax",
        "title": "Thorax – Rapid Revision",
        "content": """**Mediastinum Divisions:**
- Superior
- Inferior (anterior, middle, posterior)

**Heart:**
Right coronary artery supplies SA node.

**Lung:**
- Right lung → 3 lobes
- Left lung → 2 lobes

**Azygos Vein:**
Drains into SVC.""",
    },
    {
        "subject": "Anatomy",
        "topic": "Abdomen",
        "title": "Abdomen – Rapid Revision",
        "content": """**Portal Vein:**
Formed by:
- Splenic vein
- Superior mesenteric vein

**Portocaval Anastomosis:**
- Esophagus
- Umbilicus
- Rectum

**McBurney Point:**
Appendix surface marking (junction of lateral 1/3 and medial 2/3 of line from ASIS to umbilicus).

**Inguinal Canal Contents:**
- Spermatic cord (males)
- Round ligament (females)""",
    },
    {
        "subject": "Anatomy",
        "topic": "Head & Neck",
        "title": "Head & Neck – Rapid Revision",
        "content": """**Cranial Nerves:**
12 pairs (I–XII).

**Facial Nerve (CN VII):**
Supplies muscles of facial expression.

**Dangerous Area of Face:**
Risk of cavernous sinus thrombosis (veins drain to cavernous sinus).

**Thyroid Gland Blood Supply:**
- Superior thyroid artery (from ECA)
- Inferior thyroid artery (from thyrocervical trunk)""",
    },
    {
        "subject": "Anatomy",
        "topic": "Neuroanatomy",
        "title": "Neuroanatomy – Rapid Revision",
        "content": """**Internal Capsule:**
Common site of stroke (hemorrhagic).

**Circle of Willis:**
Cerebral arterial circle – anastomosis at base of brain.

**CSF Flow:**
Lateral ventricle → 3rd ventricle → Aqueduct of Sylvius → 4th ventricle → Subarachnoid space

**Broca's Area:**
Motor speech area (frontal lobe). Damage → expressive aphasia.

**Wernicke's Area:**
Sensory speech area (temporal lobe). Damage → receptive aphasia.""",
    },
    {
        "subject": "Anatomy",
        "topic": "Embryology",
        "title": "Embryology – Rapid Revision",
        "content": """**Pharyngeal Arches:**
- 1st arch nerve → Trigeminal (CN V)
- 2nd arch nerve → Facial (CN VII)

**Neural Tube Defects:**
- Spina bifida
- Anencephaly
- Meningocele

**Placenta:**
Derived from trophoblast.

**Fetal Circulation:**
Ductus arteriosus connects pulmonary artery to aorta (closes → ligamentum arteriosum).""",
    },
    {
        "subject": "Anatomy",
        "topic": "Histology",
        "title": "Histology – Rapid Revision",
        "content": """**Epithelium Types:**
- Squamous
- Cuboidal
- Columnar
- Transitional

**Liver:**
Hexagonal lobules. Central vein. Portal triad at corners.

**Kidney:**
Functional unit → Nephron

**Cartilage:**
Avascular (no blood vessels). Types: hyaline, elastic, fibrocartilage.""",
    },
    {
        "subject": "Anatomy",
        "topic": "Brachial Plexus",
        "title": "Brachial Plexus – Rapid Revision",
        "content": """**Roots:** C5-T1

**Trunks:**
- Upper (C5-C6)
- Middle (C7)
- Lower (C8-T1)

**Cords:**
- Lateral
- Posterior
- Medial

**Terminal Branches (MARMU):**
- Musculocutaneous (lateral cord)
- Axillary (posterior cord)
- Radial (posterior cord)
- Median (lateral + medial cord)
- Ulnar (medial cord)""",
    },
    {
        "subject": "Anatomy",
        "topic": "Osteology",
        "title": "Osteology – Rapid Revision",
        "content": """**Longest Bone:** Femur

**Smallest Bone:** Stapes

**Funny Bone:** Ulnar nerve behind medial epicondyle of humerus

**Ossification:**
- Primary centers (appear in fetal life)
- Secondary centers (appear after birth)

**Total Bones in Adult:** 206""",
    },
    {
        "subject": "Anatomy",
        "topic": "Cardiovascular System",
        "title": "Cardiovascular System – Rapid Revision",
        "content": """**Conducting System:**
SA node → AV node → Bundle of His → Bundle branches → Purkinje fibers

**Coronary Dominance:**
Usually right dominant (PDA from RCA).

**Aorta Parts:**
- Ascending aorta
- Arch of aorta (brachiocephalic, left CCA, left subclavian)
- Descending aorta (thoracic + abdominal)""",
    },
    {
        "subject": "Anatomy",
        "topic": "Gross Anatomy",
        "title": "Gross Anatomy – Rapid Revision",
        "content": """**Anatomical Position:**
Standard body reference position (erect, arms at sides, palms forward).

**Planes:**
- Sagittal (left/right)
- Coronal (anterior/posterior)
- Transverse (superior/inferior)

**Terms:**
- Medial / Lateral
- Proximal / Distal
- Superficial / Deep""",
    },
    {
        "subject": "Anatomy",
        "topic": "High Yield One-Liners",
        "title": "Anatomy – High Yield One-Liners",
        "content": """- Femur is the longest bone.
- Stapes is the smallest bone.
- Median nerve passes through carpal tunnel.
- SA node is pacemaker of heart.
- Internal capsule is commonly affected in stroke.
- Facial nerve supplies facial expression muscles.
- Sciatic nerve is the largest nerve.
- Appendix pain shifts to right iliac fossa (McBurney's point).
- Broca's area controls speech production.
- Circle of Willis is the most common site of berry aneurysm.""",
    },
    {
        "subject": "Anatomy",
        "topic": "Mnemonics",
        "title": "Anatomy – Important Mnemonics",
        "content": """**Carpal Bones:**
Some Lovers Try Positions That They Can't Handle
(Scaphoid, Lunate, Triquetral, Pisiform, Trapezium, Trapezoid, Capitate, Hamate)

**Cranial Nerves:**
On Old Olympus Towering Tops, A Finn And German Viewed Some Hops

**Branches of External Carotid:**
Some Anatomists Like Freaking Out Poor Medical Students
(Superior thyroid, Ascending pharyngeal, Lingual, Facial, Occipital, Posterior auricular, Maxillary, Superficial temporal)

**Rotator Cuff (SITS):**
Supraspinatus, Infraspinatus, Teres minor, Subscapularis

**Femoral Triangle Contents (NAVEL):**
Nerve, Artery, Vein, Empty space, Lymphatics""",
    },
    {
        "subject": "Anatomy",
        "topic": "PYQ Pearls",
        "title": "Anatomy – PYQ Pearls",
        "content": """- Nerve injured in wrist drop → Radial nerve
- Nerve in carpal tunnel → Median nerve
- Largest artery → Aorta
- Functional unit of kidney → Nephron
- Blood supply of femoral head → Medial circumflex femoral artery
- Pacemaker of heart → SA node
- Common site of berry aneurysm → Circle of Willis""",
    },
    {
        "subject": "Anatomy",
        "topic": "Viva Questions",
        "title": "Anatomy – Viva Questions",
        "content": """**1. Boundaries of femoral triangle?**
Roof: fascia lata. Floor: iliopsoas, pectineus, adductor longus.
Boundaries: Inguinal ligament (superior), Sartorius (lateral), Adductor longus (medial).

**2. What is Erb's palsy?**
Upper brachial plexus injury (C5-C6). Waiter's tip deformity – arm adducted, medially rotated, forearm pronated.

**3. Define portocaval anastomosis.**
Connections between portal and systemic venous systems. Sites: lower esophagus, umbilicus, rectum, retroperitoneal.

**4. Name branches of facial nerve.**
Temporal, Zygomatic, Buccal, Marginal mandibular, Cervical (To Zanzibar By Motor Car).

**5. Explain Circle of Willis.**
Arterial anastomosis at base of brain formed by ACA, AComA, ICA, PComA, PCA, and basilar artery.

**6. What are cranial nerves?**
12 pairs of nerves arising from brain. I & II from cerebrum, III-XII from brainstem.

**7. Describe brachial plexus.**
Network of nerves from C5-T1 supplying upper limb. Roots → Trunks → Divisions → Cords → Branches.

**8. What is Broca's area?**
Motor speech area in inferior frontal gyrus. Damage causes expressive (non-fluent) aphasia.

**9. Layers of scalp?**
SCALP: Skin, Connective tissue, Aponeurosis, Loose areolar tissue, Pericranium.

**10. Histology of liver?**
Hexagonal lobules with central vein. Portal triad at corners (hepatic artery, portal vein, bile duct). Sinusoids with Kupffer cells.""",
    },
]

# ─── MCQs ────────────────────────────────────────────────────────────────────

ANATOMY_QUESTIONS = [
    {
        "subject": "Anatomy",
        "topic": "Lower Limb",
        "question": "Largest nerve in the body?",
        "options": ["Femoral nerve", "Sciatic nerve", "Obturator nerve", "Tibial nerve"],
        "correct_answer": "Sciatic nerve",
        "explanation": "The sciatic nerve (L4-S3) is the largest and longest nerve in the body, supplying the posterior thigh and entire leg below the knee.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Osteology",
        "question": "Smallest bone in the human body?",
        "options": ["Incus", "Stapes", "Malleus", "Hyoid"],
        "correct_answer": "Stapes",
        "explanation": "Stapes is the smallest bone in the body, located in the middle ear. It measures approximately 3mm.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Upper Limb",
        "question": "Which nerve is affected in carpal tunnel syndrome?",
        "options": ["Ulnar nerve", "Radial nerve", "Median nerve", "Musculocutaneous nerve"],
        "correct_answer": "Median nerve",
        "explanation": "The median nerve passes through the carpal tunnel along with flexor tendons. Compression causes numbness in lateral 3.5 fingers.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Cardiovascular System",
        "question": "Pacemaker of the heart is?",
        "options": ["AV node", "SA node", "Bundle of His", "Purkinje fibers"],
        "correct_answer": "SA node",
        "explanation": "SA node (sinoatrial node) is the pacemaker of the heart with an intrinsic rate of 60-100 bpm. Located in the right atrium.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Neuroanatomy",
        "question": "Most common site of berry aneurysm?",
        "options": ["Basilar artery", "Circle of Willis", "MCA", "Vertebral artery"],
        "correct_answer": "Circle of Willis",
        "explanation": "Berry aneurysms most commonly occur at the junction of the anterior communicating artery with the ACA in the Circle of Willis.",
        "difficulty": "medium",
    },
    {
        "subject": "Anatomy",
        "topic": "Upper Limb",
        "question": "Erb's palsy involves injury to which roots?",
        "options": ["C5-C6", "C8-T1", "C7", "C5-T1"],
        "correct_answer": "C5-C6",
        "explanation": "Erb's palsy (upper brachial plexus injury) involves C5-C6 roots causing waiter's tip deformity.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Upper Limb",
        "question": "Nerve injured in wrist drop?",
        "options": ["Median nerve", "Ulnar nerve", "Radial nerve", "Axillary nerve"],
        "correct_answer": "Radial nerve",
        "explanation": "Radial nerve injury causes wrist drop due to paralysis of wrist extensors. Common in mid-shaft humerus fractures.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Abdomen",
        "question": "Portal vein is formed by the union of?",
        "options": ["Splenic vein + IVC", "Splenic vein + SMV", "IMV + SMV", "Hepatic veins"],
        "correct_answer": "Splenic vein + SMV",
        "explanation": "Portal vein is formed behind the neck of pancreas by the union of splenic vein and superior mesenteric vein (SMV).",
        "difficulty": "medium",
    },
    {
        "subject": "Anatomy",
        "topic": "Head & Neck",
        "question": "Facial nerve supplies?",
        "options": ["Muscles of mastication", "Muscles of facial expression", "Tongue muscles", "Pharyngeal muscles"],
        "correct_answer": "Muscles of facial expression",
        "explanation": "Facial nerve (CN VII) supplies all muscles of facial expression. Muscles of mastication are supplied by CN V (trigeminal).",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Lower Limb",
        "question": "Blood supply of femoral head is from?",
        "options": ["Lateral circumflex femoral artery", "Medial circumflex femoral artery", "Profunda femoris", "Femoral artery"],
        "correct_answer": "Medial circumflex femoral artery",
        "explanation": "Medial circumflex femoral artery is the major blood supply to the femoral head. Its damage in neck of femur fractures leads to avascular necrosis.",
        "difficulty": "medium",
    },
    {
        "subject": "Anatomy",
        "topic": "Lower Limb",
        "question": "Foot drop is caused by injury to which nerve?",
        "options": ["Tibial nerve", "Common peroneal nerve", "Femoral nerve", "Sciatic nerve"],
        "correct_answer": "Common peroneal nerve",
        "explanation": "Common peroneal nerve (lateral popliteal nerve) injury causes foot drop due to paralysis of dorsiflexors. Vulnerable at neck of fibula.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Neuroanatomy",
        "question": "Broca's area is located in?",
        "options": ["Temporal lobe", "Parietal lobe", "Frontal lobe", "Occipital lobe"],
        "correct_answer": "Frontal lobe",
        "explanation": "Broca's area (motor speech area) is located in the inferior frontal gyrus (area 44, 45). Damage causes expressive aphasia.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Neuroanatomy",
        "question": "Internal capsule is most commonly affected in?",
        "options": ["Subarachnoid hemorrhage", "Stroke", "Meningitis", "Tumor"],
        "correct_answer": "Stroke",
        "explanation": "Internal capsule is supplied by lenticulostriate arteries (branches of MCA). Their rupture causes hemorrhagic stroke – the most common site.",
        "difficulty": "medium",
    },
    {
        "subject": "Anatomy",
        "topic": "Thorax",
        "question": "Right lung has how many lobes?",
        "options": ["2", "3", "4", "5"],
        "correct_answer": "3",
        "explanation": "Right lung has 3 lobes (upper, middle, lower) separated by oblique and horizontal fissures. Left lung has 2 lobes.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Embryology",
        "question": "1st pharyngeal arch is supplied by which nerve?",
        "options": ["Facial nerve", "Trigeminal nerve", "Glossopharyngeal nerve", "Vagus nerve"],
        "correct_answer": "Trigeminal nerve",
        "explanation": "1st pharyngeal arch is supplied by the trigeminal nerve (CN V). It gives rise to muscles of mastication, anterior belly of digastric, etc.",
        "difficulty": "medium",
    },
    {
        "subject": "Anatomy",
        "topic": "Histology",
        "question": "Functional unit of kidney is?",
        "options": ["Lobule", "Nephron", "Glomerulus", "Collecting duct"],
        "correct_answer": "Nephron",
        "explanation": "Nephron is the structural and functional unit of the kidney. Each kidney has approximately 1 million nephrons.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Osteology",
        "question": "Longest bone in the human body?",
        "options": ["Humerus", "Tibia", "Femur", "Fibula"],
        "correct_answer": "Femur",
        "explanation": "Femur is the longest and strongest bone in the body, approximately 1/4 of body height.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Abdomen",
        "question": "McBurney's point is the surface marking of?",
        "options": ["Gallbladder", "Appendix", "Spleen", "Kidney"],
        "correct_answer": "Appendix",
        "explanation": "McBurney's point (junction of lateral 1/3 and medial 2/3 of line from ASIS to umbilicus) is the surface marking of the base of appendix.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Brachial Plexus",
        "question": "Klumpke's palsy involves injury to which roots?",
        "options": ["C5-C6", "C7", "C8-T1", "C5-T1"],
        "correct_answer": "C8-T1",
        "explanation": "Klumpke's palsy (lower brachial plexus injury) involves C8-T1 roots causing claw hand and Horner's syndrome.",
        "difficulty": "easy",
    },
    {
        "subject": "Anatomy",
        "topic": "Cardiovascular System",
        "question": "SA node is supplied by which artery?",
        "options": ["Left coronary artery", "Right coronary artery", "Left circumflex artery", "LAD"],
        "correct_answer": "Right coronary artery",
        "explanation": "SA node is supplied by the right coronary artery in 60% of cases. In remaining cases, it's from the left circumflex artery.",
        "difficulty": "medium",
    },
]


async def seed_anatomy():
    print("Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    print(f"Connected! Database: {DATABASE_NAME}")

    # Remove existing Anatomy data to avoid duplicates
    del_q = await db.questions.delete_many({"subject": "Anatomy"})
    del_n = await db.notes.delete_many({"subject": "Anatomy"})
    print(f"Cleared existing Anatomy data: {del_q.deleted_count} questions, {del_n.deleted_count} notes")

    # Insert notes
    for note in ANATOMY_NOTES:
        note["created_at"] = datetime.now(timezone.utc)
    result_notes = await db.notes.insert_many(ANATOMY_NOTES)
    print(f"Inserted {len(result_notes.inserted_ids)} notes")

    # Insert questions
    for q in ANATOMY_QUESTIONS:
        q["created_at"] = datetime.now(timezone.utc)
    result_q = await db.questions.insert_many(ANATOMY_QUESTIONS)
    print(f"Inserted {len(result_q.inserted_ids)} questions")

    # Ensure indexes
    await db.questions.create_index("subject")
    await db.questions.create_index("topic")
    await db.notes.create_index("subject")
    await db.notes.create_index("topic")

    print("\n✓ Anatomy seed completed successfully!")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed_anatomy())
