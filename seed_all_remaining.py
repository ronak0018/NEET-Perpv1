"""
Seed all remaining 15 subjects into MongoDB (notes + MCQs).
Subjects: Biochemistry, Dermatology, ENT, Forensic Medicine, Microbiology,
OBG, Ophthalmology, Orthopaedics, Pathology, Pharmacology, Physiology,
PSM, Psychiatry, Radiology, Surgery
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

SUBJECTS = [
    "Biochemistry", "Dermatology", "ENT", "Forensic Medicine",
    "Microbiology", "Obstetrics & Gynaecology", "Ophthalmology",
    "Orthopaedics", "Pathology", "Pharmacology", "Physiology",
    "PSM", "Psychiatry", "Radiology", "Surgery",
]

# ═══════════════════════════════════════════════════════════════════
# NOTES
# ═══════════════════════════════════════════════════════════════════

ALL_NOTES = [
    # ── BIOCHEMISTRY ──────────────────────────────────────────────
    {"subject": "Biochemistry", "topic": "Enzymes", "title": "Enzymes – Rapid Revision",
     "content": """**Definition:** Biological catalysts that increase reaction rate.

**Properties:** Highly specific, not consumed, lower activation energy.

**Classification:**
1. Oxidoreductases
2. Transferases
3. Hydrolases
4. Lyases
5. Isomerases
6. Ligases

**Important Enzymes:**
- CK-MB → Myocardial infarction
- ALT/AST → Liver disease
- Amylase/Lipase → Pancreatitis

**Enzyme Inhibition:**
- Competitive: ↑ Km, same Vmax
- Non-competitive: Same Km, ↓ Vmax"""},

    {"subject": "Biochemistry", "topic": "Vitamins", "title": "Vitamins – Rapid Revision",
     "content": """**Fat Soluble:** A, D, E, K
**Water Soluble:** B complex, C

**Vitamin A:** Deficiency → Night blindness
**Vitamin D:** Deficiency → Rickets/Osteomalacia
**Vitamin C:** Deficiency → Scurvy
**Vitamin B1:** Deficiency → Beriberi
**Vitamin B3:** Deficiency → Pellagra (3 Ds: Dermatitis, Diarrhea, Dementia)
**Vitamin B12:** Deficiency → Megaloblastic anemia"""},

    {"subject": "Biochemistry", "topic": "Amino Acid Metabolism", "title": "Amino Acid Metabolism – Rapid Revision",
     "content": """**Essential Amino Acids:** PVT TIM HALL

**Phenylketonuria:** Defect in phenylalanine hydroxylase.
**Maple Syrup Urine Disease:** Defect in branched-chain amino acid metabolism.
**Homocystinuria:** Marfanoid habitus.
**Urea Cycle:** Occurs in liver.
**Hyperammonemia:** Causes encephalopathy."""},

    {"subject": "Biochemistry", "topic": "Carbohydrate Metabolism", "title": "Carbohydrate Metabolism – Rapid Revision",
     "content": """**Glycolysis:** Occurs in cytoplasm.
**TCA Cycle:** Occurs in mitochondria.
**Gluconeogenesis:** Formation of glucose from non-carbohydrate sources.

**Glycogen Storage Diseases:**
- Von Gierke → G6Pase deficiency
- Pompe → Acid maltase deficiency

**Pentose Phosphate Pathway:** Produces NADPH."""},

    {"subject": "Biochemistry", "topic": "Lipid Metabolism", "title": "Lipid Metabolism – Rapid Revision",
     "content": """**Beta Oxidation:** Occurs in mitochondria.

**Ketone Bodies:** Acetoacetate, Beta-hydroxybutyrate, Acetone

**Lipoproteins:**
- Chylomicrons → Highest triglycerides
- LDL → Bad cholesterol
- HDL → Good cholesterol

**Familial Hypercholesterolemia:** LDL receptor defect."""},

    {"subject": "Biochemistry", "topic": "Molecular Biology", "title": "Molecular Biology – Rapid Revision",
     "content": """**DNA Structure:** Double helix.
**Replication:** Occurs in S phase.
**Transcription:** DNA → RNA
**Translation:** RNA → Protein
**PCR:** Amplifies DNA.

**Blotting:**
- Southern → DNA
- Northern → RNA
- Western → Protein"""},

    {"subject": "Biochemistry", "topic": "Nucleotide Metabolism", "title": "Nucleotide Metabolism – Rapid Revision",
     "content": """**Purines:** Adenine, Guanine
**Pyrimidines:** Cytosine, Thymine, Uracil
**Gout:** Hyperuricemia due to purine metabolism disorder.
**Lesch-Nyhan Syndrome:** HGPRT deficiency.
**Allopurinol:** Xanthine oxidase inhibitor."""},

    {"subject": "Biochemistry", "topic": "Clinical Biochemistry", "title": "Clinical Biochemistry – Rapid Revision",
     "content": """**Liver Function Tests:** AST, ALT, ALP, Bilirubin
**Renal Function Tests:** Urea, Creatinine
**Cardiac Markers:** Troponin → Most specific
**ABG:** pH → 7.35–7.45

**Tumor Markers:**
- AFP → HCC
- PSA → Prostate cancer
- CA-125 → Ovarian cancer"""},

    {"subject": "Biochemistry", "topic": "High Yield One-Liners", "title": "Biochemistry – High Yield One-Liners",
     "content": """- Troponin is most specific cardiac marker.
- HDL is good cholesterol.
- Glycolysis occurs in cytoplasm.
- TCA cycle occurs in mitochondria.
- Vitamin C deficiency causes scurvy.
- Vitamin D deficiency causes rickets.
- HGPRT deficiency causes Lesch-Nyhan syndrome.
- Allopurinol inhibits xanthine oxidase.
- PCR amplifies DNA.
- Albumin maintains oncotic pressure.
- Rate limiting enzyme of glycolysis → PFK-1
- Most abundant plasma protein → Albumin"""},

    {"subject": "Biochemistry", "topic": "Mnemonics", "title": "Biochemistry – Important Mnemonics",
     "content": """**Essential Amino Acids:** PVT TIM HALL
**Pellagra:** 3 Ds (Dermatitis, Diarrhea, Dementia)
**Blotting:** Southern→DNA, Northern→RNA, Western→Protein"""},

    # ── DERMATOLOGY ───────────────────────────────────────────────
    {"subject": "Dermatology", "topic": "Papulosquamous Disorders", "title": "Papulosquamous Disorders – Rapid Revision",
     "content": """**Psoriasis:**
- Chronic inflammatory disorder
- Silvery scales on extensor surfaces
- Auspitz Sign: Pinpoint bleeding on scale removal
- Koebner Phenomenon: Lesions at trauma sites
- Histology: Munro microabscesses
- Treatment: Topical steroids, Methotrexate, Biologics

**Lichen Planus (6 Ps):**
Pruritic, Purple, Polygonal, Planar, Papules, Plaques
- Wickham Striae: White lacy lines"""},

    {"subject": "Dermatology", "topic": "Vesiculobullous Disorders", "title": "Vesiculobullous Disorders – Rapid Revision",
     "content": """**Pemphigus Vulgaris:**
- Intraepidermal blister, Nikolsky positive
- Antibody: Desmoglein 3

**Bullous Pemphigoid:**
- Subepidermal blister, Nikolsky negative

**Dermatitis Herpetiformis:**
Associated with celiac disease."""},

    {"subject": "Dermatology", "topic": "Skin Infections", "title": "Skin Infections – Rapid Revision",
     "content": """**Bacterial:**
- Impetigo: Honey-colored crust (Staph aureus)
- Erysipelas: Upper dermis
- Cellulitis: Deeper dermis

**Fungal:**
- Dermatophytes: Trichophyton, Microsporum, Epidermophyton
- KOH Mount for diagnosis
- Candidiasis: Candida albicans

**Viral:**
- Herpes Simplex: Painful vesicles
- Herpes Zoster: Dermatomal distribution
- Molluscum Contagiosum: Umbilicated papules
- Warts: HPV"""},

    {"subject": "Dermatology", "topic": "STIs & Leprosy", "title": "STIs & Leprosy – Rapid Revision",
     "content": """**Syphilis:** Treponema pallidum
- Primary: Painless chancre
- Secondary: Condyloma lata

**Leprosy:**
- Lepromatous: Numerous lesions, Lepromin negative
- Tuberculoid: Few lesions, Lepromin positive
- Type 2 reaction: ENL
- MDT: Rifampicin + Dapsone + Clofazimine"""},

    {"subject": "Dermatology", "topic": "Drug Reactions & Pigment Disorders", "title": "Drug Reactions & Pigmentary Disorders",
     "content": """**SJS:** <10% skin detachment
**TEN:** >30% skin detachment
**DRESS:** Drug rash with eosinophilia
**Fixed Drug Eruption:** Recurs at same site

**Vitiligo:** Autoimmune depigmentation
**Melasma:** Hyperpigmentation over face
**Albinism:** Tyrosinase deficiency"""},

    {"subject": "Dermatology", "topic": "Hair, Nail & CT Disorders", "title": "Hair, Nail & Connective Tissue Disorders",
     "content": """**Alopecia Areata:** Autoimmune hair loss
**Koilonychia:** Iron deficiency anemia
**Pitting Nails:** Psoriasis

**SLE:** Butterfly rash
**Dermatomyositis:** Heliotrope rash
**CREST:** Calcinosis, Raynaud, Esophageal dysmotility, Sclerodactyly, Telangiectasia"""},

    {"subject": "Dermatology", "topic": "High Yield One-Liners", "title": "Dermatology – High Yield One-Liners",
     "content": """- Auspitz sign → Psoriasis
- Nikolsky sign positive → Pemphigus vulgaris
- Honey-colored crust → Impetigo
- Umbilicated papules → Molluscum contagiosum
- Painless chancre → Primary syphilis
- ENL is Type 2 lepra reaction
- Vitiligo is autoimmune
- Heliotrope rash → Dermatomyositis
- Koilonychia → Iron deficiency
- KOH mount → Fungal infection diagnosis"""},

    # ── ENT ───────────────────────────────────────────────────────
    {"subject": "ENT", "topic": "Ear", "title": "Ear – Anatomy, Otitis Media & Hearing Loss",
     "content": """**Middle Ear Bones (MIS):** Malleus, Incus, Stapes
**Smallest Bone:** Stapes
**Organ of Hearing:** Organ of Corti
**Nerve:** Vestibulocochlear (CN VIII)

**Otitis Media:**
- Organisms: S. pneumoniae, H. influenzae
- CSOM Safe type: Tubotympanic
- CSOM Unsafe type: Atticoantral (cholesteatoma)

**Hearing Loss:**
- Rinne: Normal AC>BC; Conductive BC>AC
- Weber lateralizes to affected ear in conductive deafness
- Presbycusis: Age-related SNHL
- Noise-induced: Affects 4 kHz"""},

    {"subject": "ENT", "topic": "Nose & Sinuses", "title": "Nose & Paranasal Sinuses – Rapid Revision",
     "content": """**Little's Area:** Common site of epistaxis
**Most commonly infected sinus:** Maxillary sinus
**DNS:** Deviated nasal septum

**Nasal Polyps:**
- Ethmoidal → Bilateral
- Antrochoanal → Unilateral

**Epistaxis Management:**
- Pinch nose, Nasal packing, Cauterization"""},

    {"subject": "ENT", "topic": "Pharynx & Larynx", "title": "Pharynx & Larynx – Rapid Revision",
     "content": """**Waldeyer's Ring:** Adenoids, Tonsils, Lingual tonsils
**Quinsy:** Peritonsillar abscess
**Tonsillitis Complications:** Rheumatic fever, Glomerulonephritis

**Larynx:**
- RLN supplies all intrinsic muscles except cricothyroid
- Stridor: Upper airway obstruction sign
- Laryngomalacia: Most common congenital laryngeal anomaly

**Tumours:**
- Nasopharyngeal carcinoma: Associated with EBV
- Laryngeal carcinoma: Hoarseness
- Oral cancer most common site: Tongue"""},

    {"subject": "ENT", "topic": "Vertigo & Foreign Bodies", "title": "Vertigo & Foreign Bodies – Rapid Revision",
     "content": """**BPPV:** Most common cause of vertigo
**Meniere Disease Triad:** Vertigo, Tinnitus, Hearing loss

**Foreign Bodies:**
- Common in children
- Button battery: Emergency removal
- Airway FB: Sudden stridor"""},

    {"subject": "ENT", "topic": "High Yield One-Liners", "title": "ENT – High Yield One-Liners",
     "content": """- Stapes is smallest bone in body
- Organ of Corti is organ of hearing
- Little's area is common site of epistaxis
- Maxillary sinus most commonly infected
- Quinsy = peritonsillar abscess
- RLN supplies all intrinsic laryngeal muscles except cricothyroid
- Hoarseness is common symptom of laryngeal cancer
- BPPV is most common cause of vertigo
- Unsafe CSOM associated with cholesteatoma
- Presbycusis is age-related SNHL"""},

    # ── FORENSIC MEDICINE ─────────────────────────────────────────
    {"subject": "Forensic Medicine", "topic": "Thanatology", "title": "Thanatology – Rapid Revision",
     "content": """**Early Postmortem Changes (PALR):**
- Pallor mortis
- Algor mortis (cooling)
- Livor mortis (postmortem lividity)
- Rigor mortis (starts 1-2 hr, complete by 12 hr, disappears 24-36 hr)

**Cadaveric Spasm:** Instantaneous stiffening

**Late Changes:**
- Putrefaction
- Adipocere (moist environment)
- Mummification (dry environment)"""},

    {"subject": "Forensic Medicine", "topic": "Asphyxia", "title": "Asphyxia – Rapid Revision",
     "content": """**Types:** Hanging, Strangulation, Drowning, Suffocation

**Hanging:** Ligature mark oblique, above thyroid cartilage
**Strangulation:** Ligature mark horizontal, below thyroid cartilage
**Drowning:** Fine froth at mouth, Paltauf hemorrhages
**Cafe Coronary:** Sudden choking during eating"""},

    {"subject": "Forensic Medicine", "topic": "Toxicology", "title": "Toxicology – Rapid Revision",
     "content": """**OP Poisoning (SLUDGE):**
Salivation, Lacrimation, Urination, Defecation, GI upset, Emesis
- Treatment: Atropine + Pralidoxime

**CO Poisoning:** Cherry red color
**Methanol:** Blindness
**Opioid:** Pinpoint pupils
**Paracetamol:** Hepatotoxicity
**Lead:** Burton line

**Universal adsorbent:** Activated charcoal"""},

    {"subject": "Forensic Medicine", "topic": "Injuries & Firearms", "title": "Injuries & Firearms – Rapid Revision",
     "content": """**Incised Wound:** Length > depth
**Stab Wound:** Depth > length
**Laceration:** Irregular margins
**Defense Wounds:** On hands
**Hesitation Cuts:** Suicide

**Firearms:**
- Entry wound: Inverted margins, abrasion collar
- Exit wound: Everted margins, irregular
- Tattooing: Unburnt powder particles"""},

    {"subject": "Forensic Medicine", "topic": "Medical Jurisprudence", "title": "Medical Jurisprudence & Forensic Psychiatry",
     "content": """**Consent:** Implied, Expressed, Informed
**Age of Consent:** 18 years
**Dying Declaration:** Statement by dying person
**McNaughten Rule:** Legal test for insanity

**IPC Sections:**
- 299 → Culpable homicide
- 300 → Murder
- 304A → Negligence

**Identification:**
- DNA profiling: Most accurate
- Pelvis: Best bone for sex determination
- Fingerprints: Loop, Whorl, Arch"""},

    {"subject": "Forensic Medicine", "topic": "High Yield One-Liners", "title": "Forensic Medicine – High Yield One-Liners",
     "content": """- Rigor mortis starts in 1–2 hours
- Cherry red color → CO poisoning
- Methanol poisoning → Blindness
- OP poisoning → Atropine
- Entry wound → Inverted margins
- Exit wound → Everted margins
- Paltauf hemorrhages → Drowning
- Mummification → Dry climate
- DNA profiling → Most accurate identification
- Pelvis → Best bone for sex determination"""},

    # ── MICROBIOLOGY ──────────────────────────────────────────────
    {"subject": "Microbiology", "topic": "Bacteriology", "title": "Bacteriology – Rapid Revision",
     "content": """**TB:** Acid-fast bacillus (Mycobacterium tuberculosis)
- Ziehl-Neelsen stain
- Lowenstein-Jensen medium

**Clostridium tetani:** Causes tetanus
**MRSA:** Resistant Staphylococcus aureus
**Streptococcus pyogenes:** Rheumatic fever, Glomerulonephritis

**Gram staining:**
- Gram positive: Blue/Purple
- Gram negative: Pink/Red

**MacConkey agar:** Selective for gram negative bacteria"""},

    {"subject": "Microbiology", "topic": "Virology", "title": "Virology – Rapid Revision",
     "content": """**HIV:** Infects CD4 cells, detected by ELISA (screening), Western blot (confirmatory)
**Rabies:** Negri bodies (pathognomonic)
**Hepatitis B:** Dane particle, HBsAg (screening)
**Dengue:** Aedes aegypti vector
**COVID-19:** SARS-CoV-2, RT-PCR diagnosis"""},

    {"subject": "Microbiology", "topic": "Mycology & Parasitology", "title": "Mycology & Parasitology – Rapid Revision",
     "content": """**Candida:** Budding yeast, germ tube positive
**Aspergillus:** Acute angle (45°) branching
**Cryptococcus:** India ink positive, capsulated

**Malaria:** Anopheles mosquito vector
- P. falciparum: Most dangerous
- P. vivax: Most common in India

**Kala-azar:** Leishmania donovani, sandfly vector
**Filariasis:** Wuchereria bancrofti"""},

    {"subject": "Microbiology", "topic": "Immunology", "title": "Immunology – Rapid Revision",
     "content": """**Hypersensitivity Reactions:**
- Type I: Anaphylaxis (IgE)
- Type II: Cytotoxic (IgG/IgM)
- Type III: Immune complex
- Type IV: Delayed (T-cell mediated)

**Vaccines:**
- BCG: Live vaccine
- Rabies: Killed vaccine
- OPV: Live; IPV: Killed"""},

    {"subject": "Microbiology", "topic": "Lab Diagnosis & Hospital Infections", "title": "Lab Diagnosis & Hospital Infections",
     "content": """**Sterilization:**
- Autoclave: Moist heat (121°C, 15 psi, 15 min)
- Hot air oven: Dry heat (160°C, 1 hr)

**PCR:** Amplifies DNA
**ELISA:** Detects antigen/antibody

**Hospital Infections:**
- Hand washing prevents nosocomial infection
- MRSA: Most common nosocomial pathogen"""},

    {"subject": "Microbiology", "topic": "High Yield One-Liners", "title": "Microbiology – High Yield One-Liners",
     "content": """- Cryptococcus positive with India ink
- Ziehl-Neelsen stain for TB
- HIV infects CD4 cells
- Rabies shows Negri bodies
- IgE causes allergy (Type I)
- Autoclave uses moist heat at 121°C
- MacConkey agar for gram negative bacteria
- BCG is live vaccine
- ELISA detects antigen/antibody
- P. falciparum is most dangerous malaria"""},

    # ── OBG ───────────────────────────────────────────────────────
    {"subject": "Obstetrics & Gynaecology", "topic": "Normal Pregnancy", "title": "Normal Pregnancy – Rapid Revision",
     "content": """**Duration:** 40 weeks (280 days)
**Normal Fetal Heart Rate:** 110-160/min
**Fundal Height:** Corresponds with gestational age
**Physiological Anemia:** Normal in pregnancy (hemodilution)

**Trimesters:**
- 1st: 0-12 weeks (organogenesis)
- 2nd: 13-28 weeks
- 3rd: 29-40 weeks"""},

    {"subject": "Obstetrics & Gynaecology", "topic": "High Risk Pregnancy", "title": "High Risk Pregnancy – Rapid Revision",
     "content": """**Preeclampsia:** HTN + proteinuria after 20 weeks
**Eclampsia:** Preeclampsia + seizures (Rx: MgSO4)
**GDM:** Gestational diabetes mellitus
**Rh Incompatibility:** Anti-D prophylaxis"""},

    {"subject": "Obstetrics & Gynaecology", "topic": "Obstetric Hemorrhage", "title": "Obstetric Hemorrhage – Rapid Revision",
     "content": """**APH:**
- Placenta previa: Painless bleeding
- Abruptio placentae: Painful bleeding

**PPH:**
- Most common cause: Uterine atony
- Treatment: Oxytocin
- 4 Ts: Tone, Trauma, Tissue, Thrombin"""},

    {"subject": "Obstetrics & Gynaecology", "topic": "Gynaecology", "title": "Gynaecology – Rapid Revision",
     "content": """**Fibroid Uterus:** Most common benign uterine tumor
**Endometriosis:** Chocolate cyst, causes infertility
**PCOS:** Polycystic ovarian syndrome
**Ovarian Carcinoma:** CA-125 marker

**Contraception:**
- OCPs, IUCD, Barrier methods
- Emergency: Levonorgestrel

**Prolapse:** Cystocele, Rectocele, Uterine prolapse"""},

    {"subject": "Obstetrics & Gynaecology", "topic": "High Yield One-Liners", "title": "OBG – High Yield One-Liners",
     "content": """- Oxytocin for PPH
- Most common benign uterine tumor = Fibroid
- Endometriosis causes infertility
- Placenta previa = Painless bleeding
- Eclampsia treated with MgSO4
- Normal FHR: 110-160/min
- Most common cause of PPH: Uterine atony
- APGAR score assesses newborn at 1 and 5 min"""},

    # ── OPHTHALMOLOGY ─────────────────────────────────────────────
    {"subject": "Ophthalmology", "topic": "Glaucoma", "title": "Glaucoma – Rapid Revision",
     "content": """**Definition:** Raised intraocular pressure → optic nerve damage

**Types:**
- Open angle (chronic): Most common, painless
- Closed angle (acute): Painful, red eye, halos

**Treatment:**
- Timolol (beta blocker): Decreases aqueous production
- Pilocarpine: Constricts pupil
- Latanoprost: Increases uveoscleral outflow"""},

    {"subject": "Ophthalmology", "topic": "Cataract & Lens", "title": "Cataract & Lens – Rapid Revision",
     "content": """**Cataract:** Painless progressive vision loss
- Most common cause of curable blindness
- Treatment: Phacoemulsification + IOL

**Lens Dislocation:**
- Marfan syndrome: Upward
- Homocystinuria: Downward"""},

    {"subject": "Ophthalmology", "topic": "Retina & Uvea", "title": "Retina & Uvea – Rapid Revision",
     "content": """**Diabetic Retinopathy:**
- Non-proliferative: Microaneurysms, hard exudates
- Proliferative: Neovascularization

**Retinal Detachment:** Flashes, floaters, curtain-like vision loss

**Uveitis:** Painful red eye with photophobia
**Papilledema:** Optic disc swelling due to raised ICP"""},

    {"subject": "Ophthalmology", "topic": "Refractive Errors & Pharmacology", "title": "Refractive Errors & Ocular Pharmacology",
     "content": """**Myopia:** Corrected by concave lens
**Hypermetropia:** Corrected by convex lens
**Astigmatism:** Corrected by cylindrical lens

**Ocular Pharmacology:**
- Atropine: Mydriatic (dilates pupil)
- Timolol: Used in glaucoma
- Tropicamide: Short-acting mydriatic"""},

    {"subject": "Ophthalmology", "topic": "High Yield One-Liners", "title": "Ophthalmology – High Yield One-Liners",
     "content": """- Timolol used in glaucoma
- Cataract causes painless vision loss
- Papilledema due to raised ICP
- Myopia corrected by concave lens
- Most common cause of curable blindness: Cataract
- Diabetic retinopathy: Microaneurysms earliest sign
- Cherry red spot: Central retinal artery occlusion
- Argyll Robertson pupil: Neurosyphilis"""},

    # ── ORTHOPAEDICS ──────────────────────────────────────────────
    {"subject": "Orthopaedics", "topic": "Upper Limb Fractures", "title": "Upper Limb Fractures – Rapid Revision",
     "content": """**Colles Fracture:** Dinner fork deformity
**Supracondylar Fracture:** Common in children, Volkmann's ischemia risk
**Scaphoid Fracture:** Avascular necrosis risk (snuffbox tenderness)

**Nerve Injuries:**
- Surgical neck humerus → Axillary nerve
- Midshaft humerus → Radial nerve
- Medial epicondyle → Ulnar nerve
- Supracondylar → Median nerve"""},

    {"subject": "Orthopaedics", "topic": "Lower Limb Fractures", "title": "Lower Limb Fractures – Rapid Revision",
     "content": """**Neck of Femur:** Common in elderly, AVN risk
**Intertrochanteric:** Extracapsular
**Tibia:** Most common long bone fractured

**Complications:**
- Fat embolism after long bone fracture
- DVT after hip surgery
- Compartment syndrome: Anterior leg compartment"""},

    {"subject": "Orthopaedics", "topic": "Bone Tumours", "title": "Bone Tumours – Rapid Revision",
     "content": """**Osteosarcoma:** Sunburst appearance (most common primary malignant)
**Ewing Sarcoma:** Onion peel appearance
**Giant Cell Tumor:** Soap bubble appearance
**Osteochondroma:** Most common benign bone tumor

**Metabolic Bone Diseases:**
- Osteoporosis: Decreased bone density
- Rickets: Vitamin D deficiency (children)
- Osteomalacia: Vitamin D deficiency (adults)"""},

    {"subject": "Orthopaedics", "topic": "Joint & Paediatric Ortho", "title": "Joint & Paediatric Orthopaedics",
     "content": """**Osteoarthritis:** Degenerative, Heberden nodes
**Rheumatoid Arthritis:** Autoimmune, Swan neck deformity
**Septic Arthritis:** Emergency, joint aspiration needed

**Paediatric:**
- DDH: Developmental dysplasia of hip
- Perthes Disease: AVN of femoral head in children
- SCFE: Slipped capital femoral epiphysis"""},

    {"subject": "Orthopaedics", "topic": "High Yield One-Liners", "title": "Orthopaedics – High Yield One-Liners",
     "content": """- Most common benign bone tumor = Osteochondroma
- Most common primary malignant bone tumor = Osteosarcoma
- Compartment syndrome affects anterior leg compartment
- Fat embolism after long bone fracture
- Colles fracture: Dinner fork deformity
- Scaphoid fracture: Anatomical snuffbox tenderness
- Sunburst appearance: Osteosarcoma
- Onion peel: Ewing sarcoma"""},

    # ── PATHOLOGY ─────────────────────────────────────────────────
    {"subject": "Pathology", "topic": "General Pathology", "title": "Cell Injury, Necrosis & Inflammation",
     "content": """**Cell Injury:**
- Reversible: Cellular swelling
- Irreversible: Necrosis, Apoptosis

**Types of Necrosis:**
- Coagulative (most organs)
- Liquefactive (brain)
- Caseous (TB)
- Fat (pancreatitis)
- Gangrenous

**Inflammation:**
- Acute: Neutrophils
- Chronic: Lymphocytes, Macrophages
- Granuloma: Chronic inflammation (TB, Sarcoidosis)"""},

    {"subject": "Pathology", "topic": "Neoplasia", "title": "Neoplasia – Rapid Revision",
     "content": """**Benign vs Malignant:**
- Benign: Encapsulated, slow growth, no metastasis
- Malignant: Invasive, rapid growth, metastasis

**Carcinoma:** Epithelial origin
**Sarcoma:** Mesenchymal origin

**Tumor Markers:**
- AFP → HCC
- PSA → Prostate
- CA-125 → Ovarian
- CEA → Colorectal"""},

    {"subject": "Pathology", "topic": "Hematology", "title": "Hematology – Rapid Revision",
     "content": """**Anemias:**
- Microcytic: Iron deficiency
- Macrocytic: B12/Folate deficiency
- Normocytic: Chronic disease

**Leukemia:**
- ALL: Most common childhood leukemia
- CML: Philadelphia chromosome

**Lymphoma:**
- Hodgkin: Reed-Sternberg cells
- Non-Hodgkin: More common"""},

    {"subject": "Pathology", "topic": "Hemodynamic Disorders", "title": "Hemodynamic Disorders – Rapid Revision",
     "content": """**Virchow Triad (Thrombosis):**
1. Endothelial injury
2. Stasis
3. Hypercoagulability

**Embolism:** Most common = Pulmonary (from DVT)
**Shock Types:** Hypovolemic, Cardiogenic, Septic, Anaphylactic, Neurogenic

**Edema:** Transudate (low protein) vs Exudate (high protein)"""},

    {"subject": "Pathology", "topic": "Immunopathology & Genetics", "title": "Immunopathology & Genetic Disorders",
     "content": """**Autoimmune Diseases:**
- SLE: ANA positive
- RA: RF positive

**Genetic Disorders:**
- Down Syndrome: Trisomy 21
- Turner Syndrome: 45,XO
- Klinefelter: 47,XXY

**Amyloidosis:** Congo red stain, apple-green birefringence"""},

    {"subject": "Pathology", "topic": "High Yield One-Liners", "title": "Pathology – High Yield One-Liners",
     "content": """- Caseous necrosis → TB
- Reed-Sternberg cell → Hodgkin lymphoma
- Virchow triad → Thrombosis
- Granuloma → Chronic inflammation
- ALL: Most common childhood leukemia
- Philadelphia chromosome → CML
- Trisomy 21 → Down syndrome
- Congo red stain → Amyloidosis
- Most common embolism → Pulmonary"""},

    # ── PHARMACOLOGY ──────────────────────────────────────────────
    {"subject": "Pharmacology", "topic": "General Pharmacology", "title": "General Pharmacology – Rapid Revision",
     "content": """**Therapeutic Index:** Indicates drug safety (TD50/ED50)
**First Pass Metabolism:** In liver
**Bioavailability:** IV = 100%

**Drug Interactions:**
- Enzyme inducers: Rifampicin, Phenytoin, Carbamazepine
- Enzyme inhibitors: Cimetidine, Ketoconazole, Erythromycin"""},

    {"subject": "Pharmacology", "topic": "ANS Pharmacology", "title": "ANS Pharmacology – Rapid Revision",
     "content": """**Cholinergic:**
- Atropine: Anticholinergic (mydriasis, tachycardia)
- Neostigmine: Anticholinesterase

**Adrenergic:**
- Propranolol: Non-selective beta blocker
- Atenolol: Selective beta-1 blocker
- Adrenaline: Drug of choice in anaphylaxis"""},

    {"subject": "Pharmacology", "topic": "CNS Pharmacology", "title": "CNS Pharmacology – Rapid Revision",
     "content": """**Benzodiazepines:** Diazepam (anxiolytic, anticonvulsant)
- Flumazenil: Antagonist

**Antipsychotics:**
- Haloperidol: Typical (dopamine blocker)
- Clozapine: Atypical (agranulocytosis risk)

**Antidepressants:**
- SSRIs (Fluoxetine): First line for depression
- Lithium: Mood stabilizer (bipolar), monitor levels"""},

    {"subject": "Pharmacology", "topic": "CVS & Anticoagulants", "title": "CVS Pharmacology & Anticoagulants",
     "content": """**ACE Inhibitors:** Cause cough (bradykinin)
**Digoxin Toxicity:** Yellow vision, arrhythmias

**Anticoagulants:**
- Warfarin: Monitored by INR (PT)
- Heparin: Monitored by aPTT
- Protamine: Heparin antidote
- Vitamin K: Warfarin antidote"""},

    {"subject": "Pharmacology", "topic": "Antibiotics & Chemotherapy", "title": "Antibiotics & Chemotherapy – Rapid Revision",
     "content": """**Cell Wall Inhibitors:** Penicillin, Cephalosporins
**Protein Synthesis Inhibitors:** Aminoglycosides (nephrotoxic, ototoxic), Tetracyclines, Macrolides
**DNA Inhibitors:** Fluoroquinolones, Metronidazole

**Chemotherapy:**
- Methotrexate: DHFR inhibitor
- Cisplatin: Nephrotoxicity
- Cyclophosphamide: Hemorrhagic cystitis (prevent with Mesna)"""},

    {"subject": "Pharmacology", "topic": "Endocrine & Others", "title": "Endocrine & Other Pharmacology",
     "content": """**Diabetes:**
- Insulin: Lowers glucose
- Metformin: First line in T2DM (does NOT cause hypoglycemia)
- Sulfonylureas: Stimulate insulin secretion

**GIT:** Omeprazole (PPI)
**Renal:** Furosemide (loop diuretic)
**Toxicology:** Atropine for OP poisoning

**Antihistamines:**
- 1st gen (Diphenhydramine): Sedating
- 2nd gen (Cetirizine): Non-sedating"""},

    {"subject": "Pharmacology", "topic": "High Yield One-Liners", "title": "Pharmacology – High Yield One-Liners",
     "content": """- Warfarin monitored by INR
- Heparin monitored by aPTT
- Adrenaline: DOC in anaphylaxis
- Metformin: First line T2DM
- ACE inhibitors cause cough
- Clozapine causes agranulocytosis
- Flumazenil: Benzodiazepine antagonist
- Protamine: Heparin antidote
- Penicillin inhibits cell wall synthesis
- Aminoglycosides are nephrotoxic and ototoxic"""},

    # ── PHYSIOLOGY ────────────────────────────────────────────────
    {"subject": "Physiology", "topic": "General & Nerve-Muscle", "title": "General Physiology & Nerve-Muscle",
     "content": """**Homeostasis:** Maintains internal environment
**Resting Membrane Potential:** Due to K+ leak channels (-70 mV)
**Action Potential:** Na+ influx (depolarization), K+ efflux (repolarization)

**Neuromuscular Junction:**
- Neurotransmitter: Acetylcholine
- Receptor: Nicotinic
- Blocker: Succinylcholine (depolarizing), Tubocurarine (non-depolarizing)"""},

    {"subject": "Physiology", "topic": "CVS Physiology", "title": "CVS Physiology – Rapid Revision",
     "content": """**SA Node:** Pacemaker of heart (60-100 bpm)
**Cardiac Output:** HR × SV (normal ~5 L/min)
**Starling's Law:** ↑ Preload → ↑ Stroke volume

**Heart Sounds:**
- S1: Closure of AV valves
- S2: Closure of semilunar valves

**Blood Pressure:** Regulated by baroreceptors (carotid sinus, aortic arch)"""},

    {"subject": "Physiology", "topic": "Respiratory Physiology", "title": "Respiratory Physiology – Rapid Revision",
     "content": """**Surfactant:** Decreases surface tension (produced by Type II pneumocytes)
**CO2 Transport:** Mainly as bicarbonate (70%)
**O2 Transport:** Mainly by hemoglobin (97%)

**Lung Volumes:**
- Tidal Volume: ~500 mL
- Vital Capacity: Max air after max inspiration
- Residual Volume: Air remaining after max expiration"""},

    {"subject": "Physiology", "topic": "Renal & GIT Physiology", "title": "Renal & GIT Physiology – Rapid Revision",
     "content": """**GFR:** Normal ~125 mL/min
**ADH:** Concentrates urine (acts on collecting duct)
**Aldosterone:** Na+ reabsorption, K+ secretion

**GIT:**
- HCl secreted by parietal cells
- Intrinsic factor: Also from parietal cells (B12 absorption)
- Pepsinogen → Pepsin by HCl"""},

    {"subject": "Physiology", "topic": "Endocrine & Blood", "title": "Endocrine & Blood Physiology",
     "content": """**Insulin:** Lowers blood glucose
**Thyroxine:** Increases BMR
**Cortisol:** Stress hormone

**Blood:**
- Hemoglobin transports O2
- Normal Hb: Male 14-18 g/dL, Female 12-16 g/dL
- ESR: Raised in inflammation"""},

    {"subject": "Physiology", "topic": "Neurophysiology & Special Senses", "title": "Neurophysiology & Special Senses",
     "content": """**Broca's Area:** Motor speech (frontal lobe)
**Wernicke's Area:** Sensory speech (temporal lobe)

**Special Senses:**
- Rods: Dim light (scotopic) vision, Rhodopsin
- Cones: Color vision, Iodopsin
- Cochlea: Organ of hearing

**Reproductive:**
- FSH: Stimulates follicle growth
- LH: Triggers ovulation"""},

    {"subject": "Physiology", "topic": "High Yield One-Liners", "title": "Physiology – High Yield One-Liners",
     "content": """- Most O2 carried by hemoglobin
- Surfactant produced by Type II pneumocytes
- SA node is pacemaker
- Cardiac output = HR × SV
- GFR ~125 mL/min
- ADH concentrates urine
- Broca's area for motor speech
- Rods for dim vision
- HCl secreted by parietal cells
- RMP is -70 mV due to K+"""},

    # ── PSM ───────────────────────────────────────────────────────
    {"subject": "PSM", "topic": "Epidemiology", "title": "Epidemiology – Rapid Revision",
     "content": """**Incidence:** Measures NEW cases
**Prevalence:** Measures TOTAL (existing) cases

**Study Designs:**
- Cohort: Best for incidence (prospective)
- Case-Control: Best for rare diseases (retrospective)
- RCT: Gold standard for testing interventions
- Cross-sectional: Measures prevalence"""},

    {"subject": "PSM", "topic": "Biostatistics", "title": "Biostatistics – Rapid Revision",
     "content": """**Sensitivity:** True positive rate (rules OUT disease = SnNOut)
**Specificity:** True negative rate (rules IN disease = SpPIn)
**p value:** <0.05 = statistically significant
**Measures of Central Tendency:** Mean, Median, Mode

**Tests:**
- Chi-square: Categorical data
- t-test: Compare 2 means
- ANOVA: Compare >2 means"""},

    {"subject": "PSM", "topic": "Nutrition & Communicable Diseases", "title": "Nutrition & Communicable Diseases",
     "content": """**PEM:**
- Marasmus: Calorie deficiency
- Kwashiorkor: Protein deficiency

**Vitamin A:** Night blindness; Bitot spots
**Iodine Deficiency:** Goiter

**Communicable Diseases:**
- TB: DOTS treatment
- Malaria: Chloroquine (P. vivax)
- Dengue: Aedes aegypti
- HIV: NACO program"""},

    {"subject": "PSM", "topic": "NCD & Health Programs", "title": "NCD & National Health Programs",
     "content": """**NCDs:** Diabetes, Hypertension, Cancer, CVD
**NPCDCS:** National Programme for NCD

**National Health Programs:**
- NTEP: National TB Elimination Program
- UIP: Universal Immunization Programme
- RMNCHA: Reproductive, Maternal, Newborn, Child, Adolescent Health

**Prevention Levels:**
1. Primordial
2. Primary
3. Secondary
4. Tertiary"""},

    {"subject": "PSM", "topic": "Environment & Occupational Health", "title": "Environment & Occupational Health",
     "content": """**Water Purification:**
- Chlorination: Most common method
- Horrock's apparatus: Tests residual chlorine

**Biomedical Waste:**
- Yellow: Incineration
- Red: Autoclaving
- Blue: Autoclaving/Chemical

**Occupational Diseases:**
- Silicosis: Silica exposure
- Asbestosis: Asbestos
- Byssinosis: Cotton dust"""},

    {"subject": "PSM", "topic": "Demography & MCH", "title": "Demography & Maternal-Child Health",
     "content": """**Crude Birth Rate:** Births/1000 population/year
**Total Fertility Rate:** Average children per woman
**IMR:** Infant mortality rate (deaths <1 year per 1000 live births)

**Immunization Schedule:**
- BCG: At birth
- OPV: 0, 6, 10, 14 weeks
- Measles: 9 months"""},

    {"subject": "PSM", "topic": "High Yield One-Liners", "title": "PSM – High Yield One-Liners",
     "content": """- Sensitivity = True positive rate
- Specificity = True negative rate
- Cohort study best for incidence
- DOTS used in TB control
- Vaccine efficacy measured by field trials
- Chlorination: Most common water purification
- Silicosis: Most common occupite/occupational lung disease
- p < 0.05 is significant
- RCT: Gold standard study design
- IMR: Best indicator of health status"""},

    # ── PSYCHIATRY ────────────────────────────────────────────────
    {"subject": "Psychiatry", "topic": "Psychotic Disorders", "title": "Psychotic Disorders – Rapid Revision",
     "content": """**Schizophrenia:**
- Positive symptoms: Delusions, Hallucinations
- Negative symptoms: Flat affect, Alogia
- Dopamine hypothesis
- Treatment: Antipsychotics (Haloperidol, Risperidone)

**Brief Psychotic Disorder:** <1 month
**Schizophreniform:** 1-6 months"""},

    {"subject": "Psychiatry", "topic": "Mood & Anxiety Disorders", "title": "Mood & Anxiety Disorders – Rapid Revision",
     "content": """**Depression:**
- SSRIs first line (Fluoxetine)
- Serotonin hypothesis

**Bipolar Disorder:**
- Lithium: First line mood stabilizer
- Monitor: Thyroid, Renal function

**Anxiety:**
- GAD: Excessive worry
- Panic Disorder: Sudden attacks
- OCD: Obsessions + Compulsions (SSRI + CBT)"""},

    {"subject": "Psychiatry", "topic": "Substance Use & Personality", "title": "Substance Use & Personality Disorders",
     "content": """**Alcohol Withdrawal:**
- Delirium tremens (48-72 hrs)
- Treatment: Benzodiazepines (Lorazepam)

**Opioid Overdose:** Naloxone (antidote)

**Personality Disorders:**
- Cluster A: Odd (Paranoid, Schizoid, Schizotypal)
- Cluster B: Dramatic (Antisocial, Borderline, Histrionic, Narcissistic)
- Cluster C: Anxious (Avoidant, Dependent, OCPD)"""},

    {"subject": "Psychiatry", "topic": "Child Psychiatry & Others", "title": "Child Psychiatry & Other Disorders",
     "content": """**ADHD:** Inattention, Hyperactivity, Impulsivity
- Treatment: Methylphenidate

**Autism:** Social impairment, Repetitive behavior

**Eating Disorders:**
- Anorexia Nervosa: Fear of weight gain
- Bulimia: Binge + Purge

**Sleep Disorders:**
- Narcolepsy: Excessive daytime sleepiness
- Insomnia: Difficulty sleeping"""},

    {"subject": "Psychiatry", "topic": "High Yield One-Liners", "title": "Psychiatry – High Yield One-Liners",
     "content": """- Lithium used in bipolar disorder
- Clozapine causes agranulocytosis
- SSRIs first line for depression
- Delirium tremens in alcohol withdrawal
- Naloxone for opioid overdose
- Methylphenidate for ADHD
- Dopamine hypothesis in schizophrenia
- CBT commonly used psychotherapy
- Cluster B: Dramatic personality disorders
- Flumazenil: BZD antagonist"""},

    # ── RADIOLOGY ─────────────────────────────────────────────────
    {"subject": "Radiology", "topic": "Imaging Modalities", "title": "Imaging Modalities – Rapid Revision",
     "content": """**X-ray:** Dense structures appear white (radiopaque)
**CT Scan:** Best for acute bleed (head)
**MRI:** Best for soft tissue imaging; Contraindicated in pacemaker
**Ultrasound:** No radiation, Safe in pregnancy

**Nuclear Medicine:**
- PET scan: Detects metabolic activity (FDG)
- Technetium-99m: Most commonly used isotope"""},

    {"subject": "Radiology", "topic": "Contrast & Interventional", "title": "Contrast Studies & Interventional Radiology",
     "content": """**Contrast Studies:**
- Barium swallow: Esophagus
- Barium meal: Stomach
- Barium enema: Colon
- IVP/IVU: Kidneys and urinary tract

**Interventional Radiology:**
- Angioplasty: Balloon dilatation
- Embolization: Stops bleeding"""},

    {"subject": "Radiology", "topic": "Radiation Physics & Protection", "title": "Radiation Physics & Protection",
     "content": """**Gray (Gy):** Measures absorbed dose
**Sievert (Sv):** Measures biological effect
**ALARA Principle:** As Low As Reasonably Achievable

**Radiation Protection:**
- Time: Minimize exposure
- Distance: Inverse square law
- Shielding: Lead aprons"""},

    {"subject": "Radiology", "topic": "High Yield One-Liners", "title": "Radiology – High Yield One-Liners",
     "content": """- MRI contraindicated in pacemaker
- Ultrasound uses sound waves, safe in pregnancy
- CT scan best for acute intracranial bleed
- MRI best for soft tissue
- PET scan detects metabolic activity
- ALARA principle in radiation protection
- Barium swallow for esophageal study
- Gray measures absorbed radiation dose"""},

    # ── SURGERY ───────────────────────────────────────────────────
    {"subject": "Surgery", "topic": "General Surgery", "title": "General Surgery – Rapid Revision",
     "content": """**Wound Healing Phases:**
1. Hemostasis
2. Inflammation
3. Proliferation
4. Remodeling

**Shock:**
- Hypovolemic: Blood/fluid loss
- Septic: Infection (warm shock → cold shock)
- Cardiogenic: Heart failure

**Fluid Replacement:**
- Ringer Lactate: Most physiological
- Normal Saline: 0.9% NaCl"""},

    {"subject": "Surgery", "topic": "GIT Surgery", "title": "GIT Surgery – Rapid Revision",
     "content": """**Appendicitis:**
- McBurney's point tenderness
- Pain shifts from periumbilical to RIF

**Intestinal Obstruction:**
- Features: Pain, vomiting, distension, constipation
- X-ray: Multiple air-fluid levels

**Hemorrhoids:** Most common anorectal disorder
**Fistula-in-Ano:** Goodsall's rule"""},

    {"subject": "Surgery", "topic": "Hepatobiliary & Breast", "title": "Hepatobiliary & Breast Surgery",
     "content": """**Gallstones:**
- Common in females (Fat, Forty, Fertile, Fair)
- Complications: Cholecystitis, Cholangitis, Pancreatitis
- Treatment: Cholecystectomy

**Breast:**
- Fibroadenoma: Most common benign tumor (young females)
- Carcinoma: Most common in upper outer quadrant
- Screening: Mammography"""},

    {"subject": "Surgery", "topic": "Thyroid & Urology", "title": "Thyroid & Urology – Rapid Revision",
     "content": """**Thyroid Cancer:**
- Papillary: Most common (Orphan Annie eyes)
- Medullary: Calcitonin marker
- Follicular: Hematogenous spread

**Urology:**
- BPH: Common in elderly men, obstructive symptoms
- Renal Stones: Colicky pain, CT KUB best investigation
- Wilms Tumor: Most common renal tumor in children"""},

    {"subject": "Surgery", "topic": "Trauma & Vascular", "title": "Trauma & Vascular Surgery",
     "content": """**Trauma:**
- ABC protocol (Airway, Breathing, Circulation)
- Splenic injury: Most common organ injured in blunt abdominal trauma
- Surgical oncology: TNM staging

**Vascular:**
- Varicose Veins: Trendelenburg test
- DVT: Homan's sign
- AAA: Pulsatile abdominal mass

**Burns:**
- Rule of 9s for BSA estimation
- Parkland formula: 4 mL × kg × %BSA"""},

    {"subject": "Surgery", "topic": "Paediatric Surgery", "title": "Paediatric Surgery – Rapid Revision",
     "content": """**Hirschsprung Disease:** Absence of ganglion cells, transition zone on barium enema
**TEF (Tracheoesophageal Fistula):** H-type most common isolated
**Pyloric Stenosis:** Non-bilious projectile vomiting, olive-shaped mass
**Intussusception:** Sausage-shaped mass, red currant jelly stools"""},

    {"subject": "Surgery", "topic": "High Yield One-Liners", "title": "Surgery – High Yield One-Liners",
     "content": """- Appendicitis pain shifts to RIF
- Rule of 9s in burns
- Splenic injury: Most common in blunt abdominal trauma
- Fibroadenoma: Most common benign breast tumor
- Papillary carcinoma: Most common thyroid cancer
- Gallstones: Fat, Forty, Fertile, Fair
- BPH common in elderly men
- Parkland formula for burns fluid resuscitation
- Hirschsprung: Absence of ganglion cells
- TNM staging for surgical oncology"""},
]

# ═══════════════════════════════════════════════════════════════════
# MCQs
# ═══════════════════════════════════════════════════════════════════

ALL_QUESTIONS = [
    # ── BIOCHEMISTRY MCQs ─────────────────────────────────────────
    {"subject": "Biochemistry", "topic": "Clinical Biochemistry", "question": "Most specific cardiac marker?",
     "options": ["CK-MB", "Troponin", "LDH", "AST"], "correct_answer": "Troponin",
     "explanation": "Troponin (I and T) is the most specific and sensitive cardiac marker for myocardial infarction.", "difficulty": "easy"},

    {"subject": "Biochemistry", "topic": "Vitamins", "question": "Vitamin deficiency causing scurvy?",
     "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], "correct_answer": "Vitamin C",
     "explanation": "Vitamin C (ascorbic acid) deficiency causes scurvy characterized by bleeding gums, petechiae, and poor wound healing.", "difficulty": "easy"},

    {"subject": "Biochemistry", "topic": "Carbohydrate Metabolism", "question": "Site of TCA cycle?",
     "options": ["Cytoplasm", "Mitochondria", "Nucleus", "ER"], "correct_answer": "Mitochondria",
     "explanation": "TCA (Krebs) cycle occurs in the mitochondrial matrix.", "difficulty": "easy"},

    {"subject": "Biochemistry", "topic": "Nucleotide Metabolism", "question": "Defect in Lesch-Nyhan syndrome?",
     "options": ["G6PD deficiency", "HGPRT deficiency", "ADA deficiency", "PNP deficiency"], "correct_answer": "HGPRT deficiency",
     "explanation": "Lesch-Nyhan syndrome is caused by HGPRT deficiency leading to hyperuricemia, self-mutilation, and intellectual disability.", "difficulty": "medium"},

    {"subject": "Biochemistry", "topic": "Lipid Metabolism", "question": "Good cholesterol?",
     "options": ["LDL", "VLDL", "HDL", "Chylomicrons"], "correct_answer": "HDL",
     "explanation": "HDL (High-Density Lipoprotein) is called good cholesterol as it removes cholesterol from arteries.", "difficulty": "easy"},

    {"subject": "Biochemistry", "topic": "Carbohydrate Metabolism", "question": "Rate limiting enzyme of glycolysis?",
     "options": ["Hexokinase", "PFK-1", "Pyruvate kinase", "Enolase"], "correct_answer": "PFK-1",
     "explanation": "Phosphofructokinase-1 (PFK-1) is the rate-limiting enzyme of glycolysis.", "difficulty": "medium"},

    {"subject": "Biochemistry", "topic": "Molecular Biology", "question": "Southern blot detects?",
     "options": ["RNA", "Protein", "DNA", "Lipids"], "correct_answer": "DNA",
     "explanation": "Southern blot is used to detect specific DNA sequences. Northern=RNA, Western=Protein.", "difficulty": "easy"},

    {"subject": "Biochemistry", "topic": "Enzymes", "question": "In competitive inhibition, which parameter changes?",
     "options": ["Vmax increases", "Km increases", "Km decreases", "Vmax decreases"], "correct_answer": "Km increases",
     "explanation": "In competitive inhibition, Km increases (decreased affinity) while Vmax remains unchanged.", "difficulty": "medium"},

    # ── DERMATOLOGY MCQs ──────────────────────────────────────────
    {"subject": "Dermatology", "topic": "Vesiculobullous Disorders", "question": "Nikolsky sign positive in?",
     "options": ["Bullous pemphigoid", "Pemphigus vulgaris", "DH", "Eczema"], "correct_answer": "Pemphigus vulgaris",
     "explanation": "Nikolsky sign (skin peeling on lateral pressure) is positive in Pemphigus vulgaris (intraepidermal blister).", "difficulty": "easy"},

    {"subject": "Dermatology", "topic": "Skin Infections", "question": "Honey-colored crust seen in?",
     "options": ["Eczema", "Impetigo", "Psoriasis", "Lichen planus"], "correct_answer": "Impetigo",
     "explanation": "Honey-colored crust is pathognomonic of impetigo, commonly caused by Staphylococcus aureus.", "difficulty": "easy"},

    {"subject": "Dermatology", "topic": "STIs & Leprosy", "question": "Organism causing syphilis?",
     "options": ["Neisseria", "Treponema pallidum", "Chlamydia", "HPV"], "correct_answer": "Treponema pallidum",
     "explanation": "Syphilis is caused by the spirochete Treponema pallidum.", "difficulty": "easy"},

    {"subject": "Dermatology", "topic": "Drug Reactions & Pigment Disorders", "question": "Autoimmune depigmentation disorder?",
     "options": ["Melasma", "Vitiligo", "Albinism", "Tinea versicolor"], "correct_answer": "Vitiligo",
     "explanation": "Vitiligo is an autoimmune disorder causing destruction of melanocytes leading to depigmented patches.", "difficulty": "easy"},

    {"subject": "Dermatology", "topic": "Hair, Nail & CT Disorders", "question": "Butterfly rash seen in?",
     "options": ["Dermatomyositis", "SLE", "Scleroderma", "RA"], "correct_answer": "SLE",
     "explanation": "Butterfly (malar) rash over both cheeks sparing nasolabial fold is characteristic of SLE.", "difficulty": "easy"},

    {"subject": "Dermatology", "topic": "Papulosquamous Disorders", "question": "Histological finding in psoriasis?",
     "options": ["Pautrier microabscess", "Munro microabscess", "Wickham striae", "Tzanck cells"], "correct_answer": "Munro microabscess",
     "explanation": "Munro microabscesses (collections of neutrophils in stratum corneum) are characteristic histological finding of psoriasis.", "difficulty": "medium"},

    {"subject": "Dermatology", "topic": "STIs & Leprosy", "question": "Lepromin test positive in which type?",
     "options": ["Lepromatous", "Borderline", "Tuberculoid", "Indeterminate"], "correct_answer": "Tuberculoid",
     "explanation": "Lepromin test is positive in tuberculoid leprosy (good cell-mediated immunity) and negative in lepromatous.", "difficulty": "medium"},

    # ── ENT MCQs ──────────────────────────────────────────────────
    {"subject": "ENT", "topic": "Ear", "question": "Smallest bone in body?",
     "options": ["Malleus", "Incus", "Stapes", "Hyoid"], "correct_answer": "Stapes",
     "explanation": "Stapes is the smallest bone in the human body, located in the middle ear.", "difficulty": "easy"},

    {"subject": "ENT", "topic": "Nose & Sinuses", "question": "Most common sinus infected?",
     "options": ["Frontal", "Ethmoid", "Maxillary", "Sphenoid"], "correct_answer": "Maxillary",
     "explanation": "Maxillary sinus is most commonly infected because its ostium is located superiorly, making drainage difficult.", "difficulty": "easy"},

    {"subject": "ENT", "topic": "Ear", "question": "Organ of hearing?",
     "options": ["Vestibule", "Organ of Corti", "Semicircular canals", "Utricle"], "correct_answer": "Organ of Corti",
     "explanation": "Organ of Corti is the sensory organ of hearing located on the basilar membrane of the cochlea.", "difficulty": "easy"},

    {"subject": "ENT", "topic": "Vertigo & Foreign Bodies", "question": "Most common cause of vertigo?",
     "options": ["Meniere disease", "BPPV", "Labyrinthitis", "Acoustic neuroma"], "correct_answer": "BPPV",
     "explanation": "BPPV (Benign Paroxysmal Positional Vertigo) is the most common cause of vertigo, caused by otoconia displacement.", "difficulty": "easy"},

    {"subject": "ENT", "topic": "Pharynx & Larynx", "question": "Commonest symptom of laryngeal carcinoma?",
     "options": ["Dysphagia", "Hoarseness", "Stridor", "Neck mass"], "correct_answer": "Hoarseness",
     "explanation": "Hoarseness is the earliest and most common symptom of laryngeal carcinoma, especially glottic tumors.", "difficulty": "easy"},

    {"subject": "ENT", "topic": "Ear", "question": "Unsafe type of CSOM is associated with?",
     "options": ["Perforation", "Cholesteatoma", "Otosclerosis", "Polyp"], "correct_answer": "Cholesteatoma",
     "explanation": "Unsafe (atticoantral) type of CSOM is associated with cholesteatoma which can cause intracranial complications.", "difficulty": "medium"},

    # ── FORENSIC MEDICINE MCQs ────────────────────────────────────
    {"subject": "Forensic Medicine", "topic": "Toxicology", "question": "Cherry red discoloration seen in?",
     "options": ["Cyanide poisoning", "CO poisoning", "OP poisoning", "Lead poisoning"], "correct_answer": "CO poisoning",
     "explanation": "Cherry red discoloration of skin and blood is seen in carbon monoxide poisoning due to carboxyhemoglobin formation.", "difficulty": "easy"},

    {"subject": "Forensic Medicine", "topic": "Toxicology", "question": "Antidote for OP poisoning?",
     "options": ["Naloxone", "Flumazenil", "Atropine", "NAC"], "correct_answer": "Atropine",
     "explanation": "Atropine (anticholinergic) is the antidote for organophosphorus poisoning. Pralidoxime reactivates AChE.", "difficulty": "easy"},

    {"subject": "Forensic Medicine", "topic": "Medical Jurisprudence", "question": "Most reliable bone for sex determination?",
     "options": ["Skull", "Femur", "Pelvis", "Mandible"], "correct_answer": "Pelvis",
     "explanation": "Pelvis is the most reliable bone for sex determination due to distinct differences between male and female pelvis.", "difficulty": "easy"},

    {"subject": "Forensic Medicine", "topic": "Injuries & Firearms", "question": "Depth greater than length injury?",
     "options": ["Incised wound", "Stab wound", "Laceration", "Abrasion"], "correct_answer": "Stab wound",
     "explanation": "In stab wounds, depth is greater than length. In incised wounds, length is greater than depth.", "difficulty": "easy"},

    {"subject": "Forensic Medicine", "topic": "Medical Jurisprudence", "question": "Most accurate identification method?",
     "options": ["Fingerprints", "DNA profiling", "Dental records", "Scars"], "correct_answer": "DNA profiling",
     "explanation": "DNA profiling (fingerprinting) is the most accurate and reliable method of identification.", "difficulty": "easy"},

    {"subject": "Forensic Medicine", "topic": "Asphyxia", "question": "Paltauf hemorrhages seen in?",
     "options": ["Hanging", "Strangulation", "Drowning", "Suffocation"], "correct_answer": "Drowning",
     "explanation": "Paltauf hemorrhages (subpleural hemorrhages in lungs) are seen in drowning.", "difficulty": "medium"},

    # ── MICROBIOLOGY MCQs ─────────────────────────────────────────
    {"subject": "Microbiology", "topic": "Mycology & Parasitology", "question": "India ink positive organism?",
     "options": ["Aspergillus", "Candida", "Cryptococcus", "Mucor"], "correct_answer": "Cryptococcus",
     "explanation": "Cryptococcus neoformans is diagnosed by India ink staining which shows the capsule as a clear halo.", "difficulty": "easy"},

    {"subject": "Microbiology", "topic": "Bacteriology", "question": "Stain used for TB diagnosis?",
     "options": ["Gram stain", "Ziehl-Neelsen", "Albert stain", "India ink"], "correct_answer": "Ziehl-Neelsen",
     "explanation": "Ziehl-Neelsen (acid-fast) stain is used for diagnosis of TB. Mycobacteria are acid-fast bacilli.", "difficulty": "easy"},

    {"subject": "Microbiology", "topic": "Virology", "question": "HIV primarily infects which cells?",
     "options": ["CD8 cells", "CD4 cells", "B cells", "NK cells"], "correct_answer": "CD4 cells",
     "explanation": "HIV primarily infects CD4+ T-helper lymphocytes, leading to immunodeficiency.", "difficulty": "easy"},

    {"subject": "Microbiology", "topic": "Immunology", "question": "Type I hypersensitivity is mediated by?",
     "options": ["IgG", "IgM", "IgE", "IgA"], "correct_answer": "IgE",
     "explanation": "Type I (immediate/anaphylactic) hypersensitivity is mediated by IgE antibodies causing mast cell degranulation.", "difficulty": "easy"},

    {"subject": "Microbiology", "topic": "Lab Diagnosis & Hospital Infections", "question": "Temperature used in autoclave?",
     "options": ["100°C", "121°C", "160°C", "180°C"], "correct_answer": "121°C",
     "explanation": "Autoclave uses moist heat at 121°C, 15 psi pressure for 15 minutes for sterilization.", "difficulty": "easy"},

    {"subject": "Microbiology", "topic": "Virology", "question": "Pathognomonic finding in rabies?",
     "options": ["Owl eye inclusion", "Negri bodies", "Guarnieri bodies", "Cowdry bodies"], "correct_answer": "Negri bodies",
     "explanation": "Negri bodies (eosinophilic cytoplasmic inclusions in hippocampal neurons) are pathognomonic of rabies.", "difficulty": "easy"},

    # ── OBG MCQs ──────────────────────────────────────────────────
    {"subject": "Obstetrics & Gynaecology", "topic": "Obstetric Hemorrhage", "question": "Most common cause of PPH?",
     "options": ["Trauma", "Uterine atony", "Retained placenta", "Coagulopathy"], "correct_answer": "Uterine atony",
     "explanation": "Uterine atony (Tone) is the most common cause of postpartum hemorrhage, accounting for ~70% of cases.", "difficulty": "easy"},

    {"subject": "Obstetrics & Gynaecology", "topic": "Obstetric Hemorrhage", "question": "Painless bleeding in pregnancy is seen in?",
     "options": ["Abruptio placentae", "Placenta previa", "Ectopic", "Molar pregnancy"], "correct_answer": "Placenta previa",
     "explanation": "Placenta previa causes painless, bright red vaginal bleeding. Abruptio placentae causes painful bleeding.", "difficulty": "easy"},

    {"subject": "Obstetrics & Gynaecology", "topic": "Gynaecology", "question": "Most common benign uterine tumor?",
     "options": ["Adenomyosis", "Fibroid", "Polyp", "Endometrioma"], "correct_answer": "Fibroid",
     "explanation": "Leiomyoma (fibroid) is the most common benign tumor of the uterus, estrogen-dependent.", "difficulty": "easy"},

    {"subject": "Obstetrics & Gynaecology", "topic": "High Risk Pregnancy", "question": "Drug of choice for eclampsia?",
     "options": ["Diazepam", "MgSO4", "Phenytoin", "Labetalol"], "correct_answer": "MgSO4",
     "explanation": "Magnesium sulfate is the drug of choice for treatment and prevention of eclamptic seizures (Pritchard/Zuspan regimen).", "difficulty": "easy"},

    {"subject": "Obstetrics & Gynaecology", "topic": "Gynaecology", "question": "Chocolate cyst is seen in?",
     "options": ["PCOS", "Endometriosis", "Fibroid", "Ovarian cancer"], "correct_answer": "Endometriosis",
     "explanation": "Chocolate cyst (endometrioma) is an ovarian cyst filled with old blood, characteristic of endometriosis.", "difficulty": "easy"},

    # ── OPHTHALMOLOGY MCQs ────────────────────────────────────────
    {"subject": "Ophthalmology", "topic": "Glaucoma", "question": "Drug used in glaucoma?",
     "options": ["Atropine", "Timolol", "Tropicamide", "Homatropine"], "correct_answer": "Timolol",
     "explanation": "Timolol (non-selective beta blocker) decreases aqueous humor production and is used in glaucoma.", "difficulty": "easy"},

    {"subject": "Ophthalmology", "topic": "Cataract & Lens", "question": "Most common cause of curable blindness?",
     "options": ["Glaucoma", "Cataract", "Trachoma", "Diabetic retinopathy"], "correct_answer": "Cataract",
     "explanation": "Cataract is the most common cause of curable (reversible) blindness worldwide.", "difficulty": "easy"},

    {"subject": "Ophthalmology", "topic": "Retina & Uvea", "question": "Papilledema is caused by?",
     "options": ["Raised IOP", "Raised ICP", "Low ICP", "Optic neuritis"], "correct_answer": "Raised ICP",
     "explanation": "Papilledema (bilateral optic disc swelling) is caused by raised intracranial pressure.", "difficulty": "easy"},

    {"subject": "Ophthalmology", "topic": "Refractive Errors & Pharmacology", "question": "Myopia is corrected by?",
     "options": ["Convex lens", "Concave lens", "Cylindrical lens", "Prism"], "correct_answer": "Concave lens",
     "explanation": "Myopia (near-sightedness) is corrected by concave (diverging) lens. Hypermetropia by convex lens.", "difficulty": "easy"},

    {"subject": "Ophthalmology", "topic": "Retina & Uvea", "question": "Earliest sign of diabetic retinopathy?",
     "options": ["Hard exudates", "Microaneurysms", "Neovascularization", "Hemorrhages"], "correct_answer": "Microaneurysms",
     "explanation": "Microaneurysms are the earliest clinical sign of diabetic retinopathy.", "difficulty": "medium"},

    # ── ORTHOPAEDICS MCQs ─────────────────────────────────────────
    {"subject": "Orthopaedics", "topic": "Bone Tumours", "question": "Most common benign bone tumor?",
     "options": ["Osteosarcoma", "Osteochondroma", "Giant cell tumor", "Chondrosarcoma"], "correct_answer": "Osteochondroma",
     "explanation": "Osteochondroma is the most common benign bone tumor, usually seen near growth plates.", "difficulty": "easy"},

    {"subject": "Orthopaedics", "topic": "Bone Tumours", "question": "Sunburst appearance on X-ray seen in?",
     "options": ["Ewing sarcoma", "Osteosarcoma", "Osteochondroma", "Chondrosarcoma"], "correct_answer": "Osteosarcoma",
     "explanation": "Osteosarcoma shows sunburst (sunray) appearance and Codman triangle on X-ray.", "difficulty": "easy"},

    {"subject": "Orthopaedics", "topic": "Upper Limb Fractures", "question": "Dinner fork deformity is seen in?",
     "options": ["Smith fracture", "Colles fracture", "Monteggia", "Galeazzi"], "correct_answer": "Colles fracture",
     "explanation": "Colles fracture (distal radius fracture with dorsal displacement) produces dinner fork deformity.", "difficulty": "easy"},

    {"subject": "Orthopaedics", "topic": "Lower Limb Fractures", "question": "Most common long bone fractured?",
     "options": ["Femur", "Humerus", "Tibia", "Fibula"], "correct_answer": "Tibia",
     "explanation": "Tibia is the most common long bone to be fractured due to its subcutaneous location.", "difficulty": "easy"},

    {"subject": "Orthopaedics", "topic": "Lower Limb Fractures", "question": "Fat embolism is seen after fracture of?",
     "options": ["Skull", "Vertebra", "Long bones", "Phalanges"], "correct_answer": "Long bones",
     "explanation": "Fat embolism syndrome occurs after long bone fractures (especially femur), presenting with petechiae, respiratory distress, and confusion.", "difficulty": "medium"},

    # ── PATHOLOGY MCQs ────────────────────────────────────────────
    {"subject": "Pathology", "topic": "General Pathology", "question": "Caseous necrosis is seen in?",
     "options": ["Infarction", "Pancreatitis", "TB", "Gangrene"], "correct_answer": "TB",
     "explanation": "Caseous (cheese-like) necrosis is characteristic of tuberculosis and is a combination of coagulative and liquefactive necrosis.", "difficulty": "easy"},

    {"subject": "Pathology", "topic": "Hematology", "question": "Reed-Sternberg cells seen in?",
     "options": ["NHL", "Hodgkin lymphoma", "CLL", "ALL"], "correct_answer": "Hodgkin lymphoma",
     "explanation": "Reed-Sternberg cells (owl-eye cells) are pathognomonic of Hodgkin lymphoma.", "difficulty": "easy"},

    {"subject": "Pathology", "topic": "Hemodynamic Disorders", "question": "Virchow triad is associated with?",
     "options": ["Embolism", "Thrombosis", "Infarction", "Edema"], "correct_answer": "Thrombosis",
     "explanation": "Virchow triad (endothelial injury, stasis, hypercoagulability) predisposes to thrombosis.", "difficulty": "easy"},

    {"subject": "Pathology", "topic": "Hematology", "question": "Most common childhood leukemia?",
     "options": ["AML", "ALL", "CLL", "CML"], "correct_answer": "ALL",
     "explanation": "Acute Lymphoblastic Leukemia (ALL) is the most common childhood malignancy.", "difficulty": "easy"},

    {"subject": "Pathology", "topic": "Immunopathology & Genetics", "question": "Trisomy 21 causes?",
     "options": ["Turner syndrome", "Down syndrome", "Klinefelter", "Edwards syndrome"], "correct_answer": "Down syndrome",
     "explanation": "Down syndrome is caused by Trisomy 21. Features include intellectual disability, epicanthal folds, and simian crease.", "difficulty": "easy"},

    {"subject": "Pathology", "topic": "Immunopathology & Genetics", "question": "Congo red stain is used for?",
     "options": ["Amyloidosis", "TB", "Fungi", "Iron"], "correct_answer": "Amyloidosis",
     "explanation": "Congo red stain shows apple-green birefringence under polarized light in amyloidosis.", "difficulty": "medium"},

    # ── PHARMACOLOGY MCQs ─────────────────────────────────────────
    {"subject": "Pharmacology", "topic": "CVS & Anticoagulants", "question": "Warfarin is monitored by?",
     "options": ["aPTT", "INR", "BT", "CT"], "correct_answer": "INR",
     "explanation": "Warfarin (vitamin K antagonist) is monitored by INR/PT. Heparin is monitored by aPTT.", "difficulty": "easy"},

    {"subject": "Pharmacology", "topic": "CVS & Anticoagulants", "question": "Antidote for heparin?",
     "options": ["Vitamin K", "Protamine", "Flumazenil", "Naloxone"], "correct_answer": "Protamine",
     "explanation": "Protamine sulfate is the specific antidote for heparin overdose.", "difficulty": "easy"},

    {"subject": "Pharmacology", "topic": "ANS Pharmacology", "question": "Drug of choice in anaphylaxis?",
     "options": ["Hydrocortisone", "Adrenaline", "Atropine", "Dopamine"], "correct_answer": "Adrenaline",
     "explanation": "Adrenaline (epinephrine) is the drug of choice in anaphylaxis – given IM (0.5 mg of 1:1000).", "difficulty": "easy"},

    {"subject": "Pharmacology", "topic": "Endocrine & Others", "question": "First line drug in Type 2 DM?",
     "options": ["Insulin", "Metformin", "Glipizide", "Acarbose"], "correct_answer": "Metformin",
     "explanation": "Metformin is the first-line drug for Type 2 DM. It does not cause hypoglycemia and reduces weight.", "difficulty": "easy"},

    {"subject": "Pharmacology", "topic": "CNS Pharmacology", "question": "Flumazenil is antagonist of?",
     "options": ["Opioids", "Benzodiazepines", "Barbiturates", "Alcohol"], "correct_answer": "Benzodiazepines",
     "explanation": "Flumazenil is a competitive antagonist at the benzodiazepine receptor. Naloxone is the opioid antagonist.", "difficulty": "easy"},

    {"subject": "Pharmacology", "topic": "Antibiotics & Chemotherapy", "question": "Penicillin acts by inhibiting?",
     "options": ["Protein synthesis", "Cell wall synthesis", "DNA synthesis", "RNA synthesis"], "correct_answer": "Cell wall synthesis",
     "explanation": "Penicillin inhibits bacterial cell wall synthesis by blocking transpeptidation (cross-linking of peptidoglycan).", "difficulty": "easy"},

    # ── PHYSIOLOGY MCQs ───────────────────────────────────────────
    {"subject": "Physiology", "topic": "Respiratory Physiology", "question": "Surfactant is produced by?",
     "options": ["Type I pneumocytes", "Type II pneumocytes", "Clara cells", "Goblet cells"], "correct_answer": "Type II pneumocytes",
     "explanation": "Surfactant (dipalmitoyl phosphatidylcholine) is produced by Type II pneumocytes, reducing surface tension.", "difficulty": "easy"},

    {"subject": "Physiology", "topic": "CVS Physiology", "question": "Pacemaker of heart?",
     "options": ["AV node", "SA node", "Bundle of His", "Purkinje fibers"], "correct_answer": "SA node",
     "explanation": "SA node is the natural pacemaker of the heart with an intrinsic rate of 60-100 bpm.", "difficulty": "easy"},

    {"subject": "Physiology", "topic": "CVS Physiology", "question": "Cardiac output formula?",
     "options": ["HR + SV", "HR × SV", "HR / SV", "HR - SV"], "correct_answer": "HR × SV",
     "explanation": "Cardiac Output = Heart Rate × Stroke Volume. Normal CO is approximately 5 L/min.", "difficulty": "easy"},

    {"subject": "Physiology", "topic": "Renal & GIT Physiology", "question": "Normal GFR is?",
     "options": ["50 mL/min", "125 mL/min", "200 mL/min", "300 mL/min"], "correct_answer": "125 mL/min",
     "explanation": "Normal GFR is approximately 125 mL/min (180 L/day). Measured by inulin clearance.", "difficulty": "easy"},

    {"subject": "Physiology", "topic": "Renal & GIT Physiology", "question": "HCl is secreted by which cells?",
     "options": ["Chief cells", "Parietal cells", "G cells", "Mucous cells"], "correct_answer": "Parietal cells",
     "explanation": "Parietal (oxyntic) cells secrete HCl and intrinsic factor in the stomach.", "difficulty": "easy"},

    {"subject": "Physiology", "topic": "General & Nerve-Muscle", "question": "Resting membrane potential is due to?",
     "options": ["Na+ ions", "K+ ions", "Ca2+ ions", "Cl- ions"], "correct_answer": "K+ ions",
     "explanation": "Resting membrane potential (-70 mV) is primarily maintained by K+ leak channels.", "difficulty": "easy"},

    # ── PSM MCQs ──────────────────────────────────────────────────
    {"subject": "PSM", "topic": "Biostatistics", "question": "Sensitivity means?",
     "options": ["True negative rate", "True positive rate", "Positive predictive value", "Negative predictive value"],
     "correct_answer": "True positive rate",
     "explanation": "Sensitivity = TP/(TP+FN) = True positive rate. High sensitivity rules OUT disease (SnNOut).", "difficulty": "easy"},

    {"subject": "PSM", "topic": "Epidemiology", "question": "Best study design for measuring incidence?",
     "options": ["Case-control", "Cohort", "Cross-sectional", "Case series"], "correct_answer": "Cohort",
     "explanation": "Cohort study (prospective) is the best study design for measuring disease incidence.", "difficulty": "easy"},

    {"subject": "PSM", "topic": "NCD & Health Programs", "question": "DOTS is used in treatment of?",
     "options": ["Malaria", "TB", "HIV", "Leprosy"], "correct_answer": "TB",
     "explanation": "DOTS (Directly Observed Treatment Short-course) is the WHO-recommended strategy for TB control.", "difficulty": "easy"},

    {"subject": "PSM", "topic": "Biostatistics", "question": "p value <0.05 means?",
     "options": ["Not significant", "Statistically significant", "Clinically significant", "Random error"],
     "correct_answer": "Statistically significant",
     "explanation": "p <0.05 means there is <5% probability that the result occurred by chance, hence statistically significant.", "difficulty": "easy"},

    {"subject": "PSM", "topic": "Environment & Occupational Health", "question": "Most common method of water purification?",
     "options": ["Boiling", "Chlorination", "Filtration", "UV radiation"], "correct_answer": "Chlorination",
     "explanation": "Chlorination is the most widely used and cost-effective method of water purification on a large scale.", "difficulty": "easy"},

    {"subject": "PSM", "topic": "Epidemiology", "question": "Gold standard study design for interventions?",
     "options": ["Cohort", "Case-control", "RCT", "Meta-analysis"], "correct_answer": "RCT",
     "explanation": "Randomized Controlled Trial (RCT) is the gold standard for testing therapeutic interventions.", "difficulty": "easy"},

    # ── PSYCHIATRY MCQs ───────────────────────────────────────────
    {"subject": "Psychiatry", "topic": "Mood & Anxiety Disorders", "question": "Drug used in bipolar disorder?",
     "options": ["Fluoxetine", "Lithium", "Diazepam", "Haloperidol"], "correct_answer": "Lithium",
     "explanation": "Lithium is the first-line mood stabilizer for bipolar disorder. Requires monitoring of thyroid and renal function.", "difficulty": "easy"},

    {"subject": "Psychiatry", "topic": "Psychotic Disorders", "question": "Clozapine side effect?",
     "options": ["Hepatotoxicity", "Agranulocytosis", "Nephrotoxicity", "Ototoxicity"], "correct_answer": "Agranulocytosis",
     "explanation": "Clozapine (atypical antipsychotic) causes agranulocytosis (1-2%), requiring regular blood counts.", "difficulty": "easy"},

    {"subject": "Psychiatry", "topic": "Mood & Anxiety Disorders", "question": "First line drug for depression?",
     "options": ["TCA", "SSRI", "MAOI", "SNRI"], "correct_answer": "SSRI",
     "explanation": "SSRIs (e.g., Fluoxetine, Sertraline) are first-line drugs for depression due to better side effect profile.", "difficulty": "easy"},

    {"subject": "Psychiatry", "topic": "Substance Use & Personality", "question": "Delirium tremens occurs in withdrawal of?",
     "options": ["Opioids", "Cannabis", "Alcohol", "Cocaine"], "correct_answer": "Alcohol",
     "explanation": "Delirium tremens (confusion, tremors, hallucinations, autonomic instability) occurs 48-72 hrs after alcohol withdrawal.", "difficulty": "easy"},

    {"subject": "Psychiatry", "topic": "Substance Use & Personality", "question": "Antidote for opioid overdose?",
     "options": ["Flumazenil", "Naloxone", "Atropine", "Protamine"], "correct_answer": "Naloxone",
     "explanation": "Naloxone is a competitive opioid receptor antagonist used in opioid overdose.", "difficulty": "easy"},

    # ── RADIOLOGY MCQs ────────────────────────────────────────────
    {"subject": "Radiology", "topic": "Imaging Modalities", "question": "MRI is contraindicated in?",
     "options": ["Pregnancy", "Pacemaker", "Children", "Renal failure"], "correct_answer": "Pacemaker",
     "explanation": "MRI uses strong magnetic fields and is absolutely contraindicated in patients with cardiac pacemakers.", "difficulty": "easy"},

    {"subject": "Radiology", "topic": "Imaging Modalities", "question": "Best imaging for soft tissue?",
     "options": ["X-ray", "CT", "MRI", "USG"], "correct_answer": "MRI",
     "explanation": "MRI provides the best soft tissue contrast and is ideal for brain, spinal cord, joints, and ligaments.", "difficulty": "easy"},

    {"subject": "Radiology", "topic": "Imaging Modalities", "question": "Investigation safe in pregnancy?",
     "options": ["CT scan", "X-ray", "Ultrasound", "PET scan"], "correct_answer": "Ultrasound",
     "explanation": "Ultrasound uses sound waves (no ionizing radiation) and is safe in pregnancy.", "difficulty": "easy"},

    {"subject": "Radiology", "topic": "Imaging Modalities", "question": "Best investigation for acute intracranial bleed?",
     "options": ["MRI", "CT scan", "X-ray", "USG"], "correct_answer": "CT scan",
     "explanation": "Non-contrast CT scan is the best initial investigation for acute intracranial hemorrhage (appears hyperdense/white).", "difficulty": "easy"},

    {"subject": "Radiology", "topic": "Radiation Physics & Protection", "question": "ALARA principle stands for?",
     "options": ["Always Lower As Required Allowance", "As Low As Reasonably Achievable", "Avoid Lethal And Radiation Accidents", "Always Limit And Reduce Activity"],
     "correct_answer": "As Low As Reasonably Achievable",
     "explanation": "ALARA (As Low As Reasonably Achievable) is the fundamental principle of radiation protection.", "difficulty": "easy"},

    # ── SURGERY MCQs ──────────────────────────────────────────────
    {"subject": "Surgery", "topic": "GIT Surgery", "question": "Appendicitis pain shifts to?",
     "options": ["LIF", "RIF", "Epigastrium", "Umbilicus"], "correct_answer": "RIF",
     "explanation": "Appendicitis pain typically starts periumbilical then shifts to RIF (McBurney's point) due to parietal peritoneal irritation.", "difficulty": "easy"},

    {"subject": "Surgery", "topic": "Trauma & Vascular", "question": "Most common organ injured in blunt abdominal trauma?",
     "options": ["Liver", "Spleen", "Kidney", "Pancreas"], "correct_answer": "Spleen",
     "explanation": "Spleen is the most commonly injured organ in blunt abdominal trauma due to its friable parenchyma.", "difficulty": "easy"},

    {"subject": "Surgery", "topic": "Hepatobiliary & Breast", "question": "Most common benign breast tumor?",
     "options": ["Phyllodes", "Fibroadenoma", "Lipoma", "Papilloma"], "correct_answer": "Fibroadenoma",
     "explanation": "Fibroadenoma is the most common benign breast tumor, common in young women (15-35 yrs), firm, mobile.", "difficulty": "easy"},

    {"subject": "Surgery", "topic": "Thyroid & Urology", "question": "Most common thyroid cancer?",
     "options": ["Follicular", "Papillary", "Medullary", "Anaplastic"], "correct_answer": "Papillary",
     "explanation": "Papillary carcinoma is the most common thyroid cancer (~80%). Shows Orphan Annie eye nuclei and psammoma bodies.", "difficulty": "easy"},

    {"subject": "Surgery", "topic": "Trauma & Vascular", "question": "Burns BSA is calculated by?",
     "options": ["Rule of 3", "Rule of 9", "Rule of 12", "Rule of 15"], "correct_answer": "Rule of 9",
     "explanation": "Wallace's Rule of 9s is used for BSA calculation in burns: Head 9%, each arm 9%, each leg 18%, trunk 36%, perineum 1%.", "difficulty": "easy"},

    {"subject": "Surgery", "topic": "Paediatric Surgery", "question": "Hirschsprung disease is due to?",
     "options": ["Absent ganglion cells", "Excess ganglion cells", "Pyloric hypertrophy", "Intussusception"],
     "correct_answer": "Absent ganglion cells",
     "explanation": "Hirschsprung disease is caused by absence of ganglion cells in the distal colon (aganglionosis), causing functional obstruction.", "difficulty": "easy"},
]


async def seed_all():
    print("Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    print(f"Connected! Database: {DATABASE_NAME}\n")

    for subject in SUBJECTS:
        # Clear existing data for this subject
        del_q = await db.questions.delete_many({"subject": subject})
        del_n = await db.notes.delete_many({"subject": subject})
        print(f"[{subject}] Cleared: {del_q.deleted_count} questions, {del_n.deleted_count} notes")

    # Insert all notes
    now = datetime.now(timezone.utc)
    for note in ALL_NOTES:
        note["created_at"] = now
    result_notes = await db.notes.insert_many(ALL_NOTES)
    print(f"\n✓ Inserted {len(result_notes.inserted_ids)} notes across {len(SUBJECTS)} subjects")

    # Insert all questions
    for q in ALL_QUESTIONS:
        q["created_at"] = now
    result_q = await db.questions.insert_many(ALL_QUESTIONS)
    print(f"✓ Inserted {len(result_q.inserted_ids)} MCQs across {len(SUBJECTS)} subjects")

    # Ensure indexes
    await db.questions.create_index("subject")
    await db.questions.create_index("topic")
    await db.notes.create_index("subject")
    await db.notes.create_index("topic")

    # Summary
    print("\n═══ SUMMARY ═══")
    for subject in SUBJECTS:
        n_count = await db.notes.count_documents({"subject": subject})
        q_count = await db.questions.count_documents({"subject": subject})
        print(f"  {subject}: {n_count} notes, {q_count} MCQs")

    total_notes = await db.notes.count_documents({})
    total_q = await db.questions.count_documents({})
    print(f"\n  TOTAL in DB: {total_notes} notes, {total_q} questions")
    print("\n✓ All subjects seeded successfully!")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed_all())
