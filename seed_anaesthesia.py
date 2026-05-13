"""
Seed Anaesthesia notes and MCQs from Complete_Anaesthesia_NEETPG_Notes.txt into MongoDB.
"""
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).resolve().parent / "backend" / ".env")

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "neetpg")

# ─── NOTES (chapter-wise) ───────────────────────────────────────────────────

ANAESTHESIA_NOTES = [
    {
        "subject": "Anaesthesia",
        "topic": "General Anaesthesia",
        "title": "General Anaesthesia – Rapid Revision",
        "content": """**Definition:** Drug-induced reversible unconsciousness with analgesia and muscle relaxation.

**Guedel Stages:**
1. Analgesia
2. Excitement
3. Surgical Anaesthesia
4. Medullary Paralysis

**IV Agents:**
- Propofol → DOC induction
- Thiopentone → Ultra-short acting
- Ketamine → Bronchodilator, increases BP
- Etomidate → Cardio-stable
- Midazolam → Amnesia

**Inhalational Agents:**
- Halothane → Hepatotoxic
- Sevoflurane → Pediatric induction
- Desflurane → Fast recovery
- Nitrous Oxide → Diffusion hypoxia

**Malignant Hyperthermia:**
- Trigger → Succinylcholine
- Treatment → Dantrolene""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Regional Anaesthesia",
        "title": "Regional Anaesthesia – Rapid Revision",
        "content": """**Types:**
- Spinal
- Epidural
- Caudal
- Nerve blocks

**Spinal Anaesthesia:**
- Site → L3-L4
- Drug → Bupivacaine

**Complications:**
- Hypotension
- PDPH (Post-Dural Puncture Headache)
- Urinary retention""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Local Anaesthetics",
        "title": "Local Anaesthetics – Rapid Revision",
        "content": """**Mechanism:** Block sodium channels.

**Amides:** Lidocaine, Bupivacaine
**Esters:** Procaine, Cocaine

**Mnemonic:** Amides have extra "i"

**Key Fact:** Bupivacaine is the most cardiotoxic LA.""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Preoperative Assessment",
        "title": "Preoperative Assessment – Rapid Revision",
        "content": """**ASA Grading:**
- ASA I → Healthy
- ASA II → Mild disease
- ASA III → Severe disease
- ASA IV → Life-threatening
- ASA V → Moribund

**Fasting Guidelines:**
- Clear fluids → 2 hr
- Light meal → 6 hr""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Airway Management",
        "title": "Airway Management – Rapid Revision",
        "content": """**Airway Devices:**
- Oropharyngeal airway
- Nasopharyngeal airway
- LMA (Laryngeal Mask Airway)
- ET Tube (Endotracheal Tube)

**Difficult Airway Predictors:**
- Mallampati III/IV
- Short neck
- Limited mouth opening""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Mechanical Ventilation",
        "title": "Mechanical Ventilation – Rapid Revision",
        "content": """**Indications:**
- Respiratory failure
- ARDS
- Apnea

**Modes:**
- Volume control
- Pressure control

**PEEP:** Prevents alveolar collapse.""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Pain Management",
        "title": "Pain Management – Rapid Revision",
        "content": """**WHO Analgesic Ladder:**
1. NSAIDs
2. Weak opioids
3. Strong opioids

**Opioids:** Morphine, Fentanyl, Tramadol""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "ICU & Critical Care",
        "title": "ICU & Critical Care – Rapid Revision",
        "content": """**Shock Types:**
- Hypovolemic
- Cardiogenic
- Septic
- Obstructive

**Key Fact:** Noradrenaline is DOC in septic shock.""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Monitoring in Anaesthesia",
        "title": "Monitoring in Anaesthesia – Rapid Revision",
        "content": """**Standard Monitoring:**
- ECG
- Pulse oximetry
- Capnography
- BP

**ETCO2 Normal:** 35–45 mmHg""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "CPR",
        "title": "CPR (Cardiopulmonary Resuscitation) – Rapid Revision",
        "content": """**Sequence:** CAB (Compression-Airway-Breathing)

**Compression Rate:** 100–120/min
**Ratio:** 30:2

**Shockable Rhythms:**
- VF (Ventricular Fibrillation)
- Pulseless VT (Ventricular Tachycardia)""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Muscle Relaxants",
        "title": "Muscle Relaxants – Rapid Revision",
        "content": """**Depolarizing:** Succinylcholine

**Non-depolarizing:**
- Vecuronium
- Rocuronium
- Atracurium

**Succinylcholine Adverse Effects:**
- Hyperkalemia
- Malignant hyperthermia""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Fluid Management",
        "title": "Fluid Management – Rapid Revision",
        "content": """**Crystalloids:** Normal saline, Ringer lactate
**Colloids:** Albumin

**Rule:** Urine output > 0.5 mL/kg/hr""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Blood Transfusion",
        "title": "Blood Transfusion – Rapid Revision",
        "content": """**Massive Transfusion:** >10 units/24 hr

**Complications:**
- Hyperkalemia
- Citrate toxicity
- Hypothermia""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Oxygen Therapy",
        "title": "Oxygen Therapy – Rapid Revision",
        "content": """**Devices:**
- Nasal cannula
- Face mask
- NRBM (Non-Rebreather Mask)
- Ventilator""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Difficult Airway",
        "title": "Difficult Airway – Rapid Revision",
        "content": """**Mallampati Classification:** I to IV

**Difficult Airway Cart:**
- Bougie
- LMA
- Fiberoptic scope""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "ABG Analysis",
        "title": "ABG Analysis – Rapid Revision",
        "content": """**Normal Values:**
- pH → 7.35–7.45
- PaCO2 → 35–45 mmHg
- HCO3 → 22–26 mEq/L

**Respiratory Acidosis:** ↑CO2
**Metabolic Acidosis:** ↓HCO3""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Shock",
        "title": "Shock – Rapid Revision",
        "content": """**Septic Shock:** Warm peripheries initially.

**Treatment:**
- Fluids
- Antibiotics
- Vasopressors""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Anaesthesia Equipment",
        "title": "Anaesthesia Equipment – Rapid Revision",
        "content": """**Boyle's Machine:** Anaesthesia workstation.
**Laryngoscope:** Macintosh blade most common.""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Sedation",
        "title": "Sedation – Rapid Revision",
        "content": """**Conscious Sedation:** Patient responds to verbal commands.

**Drugs:**
- Midazolam
- Propofol""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "High Yield One-Liners",
        "title": "Anaesthesia – High Yield One-Liners",
        "content": """- Dantrolene treats malignant hyperthermia.
- Ketamine causes dissociative anaesthesia.
- Bupivacaine is cardiotoxic.
- Succinylcholine causes hyperkalemia.
- Propofol is antiemetic.
- Noradrenaline is DOC in septic shock.
- ETCO2 normal = 35–45 mmHg.
- Mallampati predicts difficult intubation.
- MAC inversely proportional to potency.""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Mnemonics",
        "title": "Anaesthesia – Important Mnemonics",
        "content": """**Amides have extra i:** Lidocaine, Bupivacaine

**Hs & Ts (Reversible causes in cardiac arrest):**
- Hypoxia, Hypovolemia, Hypothermia
- Tamponade, Toxins, Thrombosis""",
    },
    {
        "subject": "Anaesthesia",
        "topic": "PYQ Pearls",
        "title": "Anaesthesia – PYQ Pearls",
        "content": """- Most cardiotoxic LA → Bupivacaine
- DOC for septic shock → Noradrenaline
- Trigger for malignant hyperthermia → Succinylcholine
- Most common blade → Macintosh
- Gold standard airway → Endotracheal tube""",
    },
]

# ─── MCQs ────────────────────────────────────────────────────────────────────

ANAESTHESIA_QUESTIONS = [
    {
        "subject": "Anaesthesia",
        "topic": "Local Anaesthetics",
        "question": "Most cardiotoxic local anaesthetic?",
        "options": ["Lidocaine", "Bupivacaine", "Procaine", "Ropivacaine"],
        "correct_answer": "Bupivacaine",
        "explanation": "Bupivacaine is the most cardiotoxic local anaesthetic due to its high affinity for cardiac sodium channels.",
        "difficulty": "medium",
    },
    {
        "subject": "Anaesthesia",
        "topic": "General Anaesthesia",
        "question": "Drug used for treatment of malignant hyperthermia?",
        "options": ["Dantrolene", "Succinylcholine", "Propofol", "Halothane"],
        "correct_answer": "Dantrolene",
        "explanation": "Dantrolene is the specific antidote for malignant hyperthermia. It acts by inhibiting calcium release from sarcoplasmic reticulum.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "General Anaesthesia",
        "question": "DOC for induction of anaesthesia?",
        "options": ["Thiopentone", "Propofol", "Ketamine", "Etomidate"],
        "correct_answer": "Propofol",
        "explanation": "Propofol is the drug of choice for induction due to rapid onset, smooth induction, and antiemetic properties.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "CPR",
        "question": "Which is a shockable rhythm in cardiac arrest?",
        "options": ["Asystole", "PEA", "Ventricular fibrillation", "Sinus bradycardia"],
        "correct_answer": "Ventricular fibrillation",
        "explanation": "VF and pulseless VT are shockable rhythms. Asystole and PEA are non-shockable.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Airway Management",
        "question": "Gold standard for definitive airway management?",
        "options": ["LMA", "Oropharyngeal airway", "Endotracheal tube", "Nasopharyngeal airway"],
        "correct_answer": "Endotracheal tube",
        "explanation": "Endotracheal intubation is the gold standard for definitive airway management as it provides a cuffed, secured airway.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "ICU & Critical Care",
        "question": "DOC for septic shock?",
        "options": ["Dopamine", "Noradrenaline", "Adrenaline", "Dobutamine"],
        "correct_answer": "Noradrenaline",
        "explanation": "Noradrenaline (norepinephrine) is the first-line vasopressor in septic shock as per Surviving Sepsis Campaign guidelines.",
        "difficulty": "medium",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Monitoring in Anaesthesia",
        "question": "Normal ETCO2 value is?",
        "options": ["20–30 mmHg", "35–45 mmHg", "50–60 mmHg", "25–35 mmHg"],
        "correct_answer": "35–45 mmHg",
        "explanation": "Normal end-tidal CO2 (ETCO2) is 35–45 mmHg, slightly less than arterial PaCO2.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Airway Management",
        "question": "Mallampati classification is used to predict?",
        "options": ["Blood loss", "Difficult intubation", "Cardiac risk", "Renal function"],
        "correct_answer": "Difficult intubation",
        "explanation": "Mallampati classification (I-IV) assesses oropharyngeal structures to predict difficulty of intubation.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "General Anaesthesia",
        "question": "Which inhalational agent is preferred for pediatric induction?",
        "options": ["Halothane", "Sevoflurane", "Desflurane", "Isoflurane"],
        "correct_answer": "Sevoflurane",
        "explanation": "Sevoflurane is non-irritant to airways and has rapid onset making it ideal for pediatric inhalational induction.",
        "difficulty": "medium",
    },
    {
        "subject": "Anaesthesia",
        "topic": "General Anaesthesia",
        "question": "Ketamine causes which type of anaesthesia?",
        "options": ["General anaesthesia", "Dissociative anaesthesia", "Balanced anaesthesia", "Regional anaesthesia"],
        "correct_answer": "Dissociative anaesthesia",
        "explanation": "Ketamine produces dissociative anaesthesia by blocking NMDA receptors, causing a trance-like state with analgesia.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Muscle Relaxants",
        "question": "Succinylcholine can cause all EXCEPT?",
        "options": ["Hyperkalemia", "Malignant hyperthermia", "Bradycardia", "Hypotension"],
        "correct_answer": "Hypotension",
        "explanation": "Succinylcholine causes hyperkalemia, malignant hyperthermia, bradycardia, and raised IOP. It does not typically cause hypotension.",
        "difficulty": "hard",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Regional Anaesthesia",
        "question": "Most common site for spinal anaesthesia?",
        "options": ["L1-L2", "L2-L3", "L3-L4", "L4-L5"],
        "correct_answer": "L3-L4",
        "explanation": "L3-L4 interspace is preferred as it is below the level of conus medullaris (L1-L2), reducing risk of spinal cord injury.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Regional Anaesthesia",
        "question": "Most common complication of spinal anaesthesia?",
        "options": ["Hypotension", "Cauda equina syndrome", "Epidural abscess", "Meningitis"],
        "correct_answer": "Hypotension",
        "explanation": "Hypotension due to sympathetic blockade is the most common complication of spinal anaesthesia.",
        "difficulty": "medium",
    },
    {
        "subject": "Anaesthesia",
        "topic": "CPR",
        "question": "Compression rate in CPR as per latest guidelines?",
        "options": ["60–80/min", "80–100/min", "100–120/min", "120–140/min"],
        "correct_answer": "100–120/min",
        "explanation": "AHA guidelines recommend chest compressions at a rate of 100–120 per minute with a depth of at least 2 inches.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Anaesthesia Equipment",
        "question": "Most commonly used laryngoscope blade?",
        "options": ["Miller", "Macintosh", "McCoy", "Wisconsin"],
        "correct_answer": "Macintosh",
        "explanation": "Macintosh (curved) blade is the most commonly used laryngoscope blade. It is placed in the vallecula.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "General Anaesthesia",
        "question": "Which inhalational agent causes hepatotoxicity?",
        "options": ["Sevoflurane", "Desflurane", "Halothane", "Isoflurane"],
        "correct_answer": "Halothane",
        "explanation": "Halothane causes hepatotoxicity (Halothane hepatitis) due to trifluoroacetyl metabolites causing immune-mediated liver injury.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "ABG Analysis",
        "question": "Normal arterial blood pH range is?",
        "options": ["7.25–7.35", "7.35–7.45", "7.45–7.55", "7.30–7.40"],
        "correct_answer": "7.35–7.45",
        "explanation": "Normal arterial blood pH is 7.35–7.45. Below 7.35 is acidosis and above 7.45 is alkalosis.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Preoperative Assessment",
        "question": "ASA grade I indicates?",
        "options": ["Mild systemic disease", "Healthy patient", "Severe disease", "Moribund patient"],
        "correct_answer": "Healthy patient",
        "explanation": "ASA I = Normal healthy patient with no systemic disease.",
        "difficulty": "easy",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Fluid Management",
        "question": "Minimum acceptable urine output in adults is?",
        "options": ["0.2 mL/kg/hr", "0.5 mL/kg/hr", "1.0 mL/kg/hr", "2.0 mL/kg/hr"],
        "correct_answer": "0.5 mL/kg/hr",
        "explanation": "Minimum acceptable urine output is 0.5 mL/kg/hr in adults, indicating adequate renal perfusion.",
        "difficulty": "medium",
    },
    {
        "subject": "Anaesthesia",
        "topic": "Pain Management",
        "question": "First step in WHO analgesic ladder?",
        "options": ["Weak opioids", "NSAIDs", "Strong opioids", "Nerve block"],
        "correct_answer": "NSAIDs",
        "explanation": "WHO analgesic ladder: Step 1 = Non-opioids (NSAIDs/Paracetamol), Step 2 = Weak opioids, Step 3 = Strong opioids.",
        "difficulty": "easy",
    },
]

# ─── VIVA QUESTIONS (as flash-card style notes) ──────────────────────────────

ANAESTHESIA_VIVA = [
    {
        "subject": "Anaesthesia",
        "topic": "Viva Questions",
        "title": "Anaesthesia – Viva Questions",
        "content": """**1. Define MAC.**
MAC (Minimum Alveolar Concentration) is the concentration of inhaled anaesthetic at 1 atm that prevents movement in 50% of patients in response to a surgical stimulus.

**2. What is Mallampati grading?**
A classification (I-IV) based on visualization of oropharyngeal structures (fauces, pillars, soft palate, uvula) to predict difficult intubation.

**3. Causes of failed intubation?**
Short neck, limited mouth opening, Mallampati III/IV, obesity, cervical spine pathology, tumours.

**4. Complications of spinal anaesthesia?**
Hypotension, PDPH, urinary retention, TNS, cauda equina syndrome, high spinal block.

**5. Indications of mechanical ventilation?**
Respiratory failure (Type I & II), ARDS, apnea, GCS < 8, post-operative respiratory support.

**6. Define shock.**
Shock is a state of inadequate tissue perfusion leading to cellular hypoxia and organ dysfunction.

**7. What is ETCO2?**
End-tidal CO2 measured by capnography. Normal: 35–45 mmHg. Used to confirm ETT placement and monitor ventilation.

**8. Explain CPR sequence.**
CAB: Compressions (100–120/min, 2 inches depth) → Airway (head tilt, chin lift) → Breathing (30:2 ratio).

**9. Drugs causing malignant hyperthermia?**
Succinylcholine and volatile inhalational agents (Halothane, Sevoflurane, Desflurane).

**10. Difference between spinal and epidural?**
Spinal: single shot, CSF space, rapid onset, dense block. Epidural: catheter possible, epidural space, slower onset, segmental block.""",
    },
]


async def seed_anaesthesia():
    print("Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    print(f"Connected! Database: {DATABASE_NAME}")

    # Remove existing Anaesthesia data to avoid duplicates
    del_q = await db.questions.delete_many({"subject": "Anaesthesia"})
    del_n = await db.notes.delete_many({"subject": "Anaesthesia"})
    print(f"Cleared existing Anaesthesia data: {del_q.deleted_count} questions, {del_n.deleted_count} notes")

    # Insert notes
    all_notes = ANAESTHESIA_NOTES + ANAESTHESIA_VIVA
    for note in all_notes:
        note["created_at"] = datetime.utcnow()
    result_notes = await db.notes.insert_many(all_notes)
    print(f"Inserted {len(result_notes.inserted_ids)} notes")

    # Insert questions
    for q in ANAESTHESIA_QUESTIONS:
        q["created_at"] = datetime.utcnow()
    result_q = await db.questions.insert_many(ANAESTHESIA_QUESTIONS)
    print(f"Inserted {len(result_q.inserted_ids)} questions")

    # Ensure indexes
    await db.questions.create_index("subject")
    await db.questions.create_index("topic")
    await db.notes.create_index("subject")
    await db.notes.create_index("topic")

    print("\n✓ Anaesthesia seed completed successfully!")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed_anaesthesia())
