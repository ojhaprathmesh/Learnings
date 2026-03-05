"""
============================================================
  Part B – Fine-Tuning a Small Language Model
  Dataset  : University / College FAQ (custom, 60 Q&A pairs)
  Model    : GPT-2 Small (124 M parameters) via Hugging Face
  Epochs   : 3
  Deliverables:
      • Training loss graph  →  training_loss_graph.png
      • Output comparison    →  output_comparison.png
      • Fine-tuned model     →  ./finetuned_faq/
============================================================
  Run:
      pip install transformers datasets accelerate matplotlib torch
      python partB_finetune_faq.py
============================================================
"""

# ──────────────────────────────────────────────────────────
#  STEP 0 ─ Imports & Configuration
# ──────────────────────────────────────────────────────────
import os, math, time, textwrap, warnings
warnings.filterwarnings("ignore")

import torch
import numpy as np
import matplotlib
matplotlib.use("Agg")                  # headless – no display needed
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    set_seed,
)
from datasets import Dataset

# ── Reproducibility ───────────────────────────────────────
set_seed(42)

# ── Config ────────────────────────────────────────────────
MODEL_ID   = "gpt2"          # GPT-2 Small (124 M params) – SLM
MAX_LEN    = 128             # max token length per sample
EPOCHS     = 3               # fine-tune for 3 epochs
BATCH      = 4               # per-device batch size
GRAD_ACCUM = 2               # effective batch = BATCH * GRAD_ACCUM = 8
LR         = 5e-5            # learning rate
OUTPUT_DIR = "./finetuned_faq"
DEVICE     = "cuda" if torch.cuda.is_available() else "cpu"

print(f"\nFine-tuning {MODEL_ID} | Device: {DEVICE} | Epochs: {EPOCHS}")


# ──────────────────────────────────────────────────────────
#  STEP 1 ─ University FAQ Dataset (60 Q&A pairs, 6 topics)
# ──────────────────────────────────────────────────────────
print("\n[Step 1] Building University FAQ dataset...")

RAW_FAQ = [
    # ── ADMISSIONS (10) ───────────────────────────────────
    ("What are the admission requirements for undergraduate programs?",
     "Applicants need a minimum of 60% in 10+2 examinations along with a valid entrance test score such as JEE or SAT, depending on the program."),
    ("When does the admission portal open for the new academic year?",
     "The admission portal opens every year on March 1st and closes on May 31st for undergraduate programs."),
    ("Is there an application fee for the admission process?",
     "Yes, a non-refundable application fee of Rs 500 is charged at the time of form submission."),
    ("Can international students apply for undergraduate programs?",
     "Yes, international students can apply through the International Admissions Office with valid passport copies and equivalency certificates."),
    ("What documents are required at the time of admission?",
     "Students must submit 10th and 12th mark sheets, transfer certificate, migration certificate, passport-size photographs, and character certificate."),
    ("Is there a management quota for admissions?",
     "Yes, 15% of seats are reserved under management quota. Contact the admissions office for details."),
    ("How can I check the status of my application?",
     "Log in to the student portal at admissions.university.edu and navigate to Application Status to view real-time updates."),
    ("Are there any scholarships available for new students?",
     "Merit scholarships are available for students scoring above 90% in qualifying exams. Need-based scholarships are also offered."),
    ("What is the process for cancellation of admission?",
     "Submit a written application to the Dean of Student Affairs. Refunds are processed within 30 working days per the university refund policy."),
    ("Can I change my program after admission?",
     "Program changes are allowed within the first two weeks of the semester, subject to seat availability and academic council approval."),

    # ── LIBRARY (10) ──────────────────────────────────────
    ("What are the library working hours?",
     "The central library is open Monday to Saturday from 8:00 AM to 10:00 PM and on Sundays from 10:00 AM to 5:00 PM."),
    ("How many books can a student borrow at a time?",
     "Undergraduate students can borrow up to 4 books for 14 days. Postgraduate students can borrow up to 6 books for 21 days."),
    ("How do I access e-journals and online databases?",
     "Use your university email credentials to log in at library.university.edu/eresources. Off-campus access is available via the university VPN."),
    ("What is the fine for overdue books?",
     "A fine of Rs 2 per day per book is charged after the due date. Books overdue by more than 60 days will be billed at replacement cost."),
    ("Does the library offer inter-library loan services?",
     "Yes, the library is part of the INFLIBNET network. Request inter-library loans through the reference desk with at least 5 working days notice."),
    ("How do I reserve a book that is currently on loan?",
     "Log in to the library portal and click Place Hold on the book page. You will be notified via email when it becomes available."),
    ("Is there a silent study zone in the library?",
     "Yes, the third floor is a silent study zone with individual carrels. Group study rooms on the second floor must be booked in advance."),
    ("Can alumni borrow books from the university library?",
     "Alumni can register for a courtesy library card with an annual fee of Rs 1000, allowing them to borrow up to 2 books at a time."),
    ("What referencing software does the library support?",
     "The library provides licenses for Mendeley and Zotero. Training workshops are held every semester — see the library website for schedules."),
    ("How do I report a missing or damaged book?",
     "Report missing or damaged books to the circulation desk. The student responsible will be billed for the replacement cost."),

    # ── EXAMINATIONS (10) ─────────────────────────────────
    ("When is the examination schedule published?",
     "The examination schedule is published on the university website 30 days before the start of the examination period."),
    ("How do I apply for a re-evaluation of my answer sheet?",
     "Submit a re-evaluation form at the examinations office within 10 days of result declaration. A fee of Rs 300 per subject applies."),
    ("What is the minimum attendance required to sit for exams?",
     "Students must maintain a minimum of 75% attendance in each subject to be eligible for the end-semester examination."),
    ("Can I get a copy of my evaluated answer sheet?",
     "Yes, under the Right to Information policy, you can apply for a photocopy within 15 days of result publication."),
    ("What happens if I miss an examination due to medical reasons?",
     "Submit a medical certificate from a registered doctor to the Deans office within 3 days. A make-up exam will be scheduled if approved."),
    ("How are grades calculated at the university?",
     "Grades are on a 10-point CGPA scale. Internal assessment contributes 30% and the end-semester exam contributes 70% of total marks."),
    ("Is there a provision for students with disabilities during exams?",
     "Yes, students with certified disabilities receive extra time and scribe services. Apply to the Student Welfare Office at least 2 weeks before exams."),
    ("How can I get my degree certificate after graduation?",
     "Degree certificates are issued at the annual convocation. Students who cannot attend may apply for postal dispatch through the registrars office."),
    ("What is the policy on academic misconduct during examinations?",
     "Any student guilty of malpractice faces cancellation of their paper and possible suspension. Repeat offences may result in expulsion."),
    ("How do I get my transcripts for higher studies abroad?",
     "Apply for official transcripts through the registrars office with a fee of Rs 500. Allow 5 to 7 working days for issuance."),

    # ── HOSTEL (10) ───────────────────────────────────────
    ("How do I apply for hostel accommodation?",
     "Fill in the hostel allotment form on the student portal during admission. Allotments are based on distance from hometown and merit."),
    ("What facilities are provided in the hostel?",
     "Hostels provide furnished rooms, 24-hour Wi-Fi, hot water, a common room, a gym, a mess with three daily meals, and laundry services."),
    ("What is the hostel fee per semester?",
     "Hostel fees range from Rs 25,000 to Rs 40,000 per semester depending on single or shared occupancy, excluding mess charges."),
    ("Are visitors allowed in the hostel?",
     "Visitors are permitted in the common room between 9:00 AM and 6:00 PM. They are not allowed in the residential blocks."),
    ("What is the hostel curfew timing?",
     "Students must return by 10:00 PM on weekdays and 11:00 PM on weekends. Late entry must be pre-approved by the hostel warden."),
    ("How do I raise a maintenance complaint in the hostel?",
     "Submit a maintenance request through the student portal under Hostel Services. Requests are addressed within 48 hours."),
    ("Can I change my hostel room?",
     "Room change requests are accepted at the start of each semester. Submit the request to the hostel warden with a valid reason."),
    ("What is the policy for hostel leave?",
     "Submit a leave application to the hostel warden. For leaves longer than 3 days, parental consent is required."),
    ("Is the hostel mess vegetarian only?",
     "The main mess provides both vegetarian and non-vegetarian options. A dedicated vegetarian mess is also available on request."),
    ("What security measures are in place at the hostel?",
     "The hostel has 24-hour CCTV surveillance, biometric entry, and security guards stationed at all entry points."),

    # ── IT SUPPORT (10) ───────────────────────────────────
    ("How do I get my university email account?",
     "Your university email is created automatically during admission. Credentials are sent to your personal email within 48 hours of enrollment."),
    ("What should I do if I forget my student portal password?",
     "Click Forgot Password on the portal login page. A reset link will be sent to your registered email. Contact IT support if the issue persists."),
    ("How do I connect to the campus Wi-Fi?",
     "Select UniSecure on your device and log in with your roll number and portal password. Call IT support at ext 2100 for assistance."),
    ("Is there a VPN available for off-campus access?",
     "Yes, download the VPN client from it.university.edu/vpn and authenticate with your student credentials to access all resources remotely."),
    ("How do I access Microsoft Office as a student?",
     "All enrolled students receive free Microsoft 365 access. Sign in at office.com using your university email address."),
    ("What are the IT help desk working hours?",
     "The IT help desk is open Monday to Friday from 9:00 AM to 6:00 PM. For urgent issues email itsupport@university.edu."),
    ("How do I report a cybersecurity incident?",
     "Report all cybersecurity incidents immediately to itsecurity@university.edu. Do not attempt to fix compromised devices yourself."),
    ("Can I get software installed on a lab computer?",
     "Submit a software installation request via the IT portal. Licensed software approved by the department is installed within 3 working days."),
    ("Is printing available on campus?",
     "Students get 100 free pages per month. Colour printing costs Rs 5 per page and is available at the IT centre."),
    ("How do I access my course materials online?",
     "All course materials are on the Learning Management System at lms.university.edu. Log in with your student credentials."),

    # ── FINANCE (10) ──────────────────────────────────────
    ("What are the payment methods accepted for tuition fees?",
     "Fees can be paid online via net banking, credit/debit card, or UPI through the finance portal. Demand drafts are accepted at the accounts office."),
    ("Is there an EMI option available for tuition fees?",
     "Yes, the university offers an interest-free EMI plan in 3 installments per semester. Apply through the finance office before the due date."),
    ("How do I get a fee receipt?",
     "Fee receipts are generated automatically on the student portal after successful payment and can be downloaded at any time."),
    ("What is the last date for fee payment this semester?",
     "The fee payment deadline is the 15th of the first month of each semester. A late fee of Rs 50 per day applies after this date."),
    ("How do I apply for a fee concession?",
     "Submit a fee concession application to the Student Welfare Office with proof of financial hardship. Concessions range from 10% to 50%."),
    ("Are there any grants available for research students?",
     "Research scholars can apply for the university grant of up to Rs 50,000 per year for equipment and travel through the research office."),
    ("How do I get a no-dues certificate?",
     "Apply through the student portal after clearing all dues with the library, hostel, and accounts office."),
    ("Can I get a refund if I withdraw from a course?",
     "Course withdrawal refunds follow the university refund schedule. Full refunds are given up to the 10th day of the semester."),
    ("How is the scholarship amount disbursed?",
     "Scholarships are credited directly to the students registered bank account within 30 days of scholarship committee approval."),
    ("What financial aid options are available for students from low-income families?",
     "Low-income students can apply for the Chief Minister Scholarship, the university need-based grant, and bank education loans via the finance office."),
]

# Format each pair into a causal LM prompt
def fmt(q, a):
    return f"Question: {q}\nAnswer: {a}<|endoftext|>"

samples   = [fmt(q, a) for q, a in RAW_FAQ]
split_idx = int(len(samples) * 0.80)          # 80/20 split
train_texts = samples[:split_idx]             # 48 samples
val_texts   = samples[split_idx:]             # 12 samples

print(f"Samples: {len(samples)} | Train: {len(train_texts)} | Val: {len(val_texts)}")


# ──────────────────────────────────────────────────────────
#  STEP 2 ─ Load Tokenizer & Pretrained Model
# ──────────────────────────────────────────────────────────
print("\n[Step 2] Loading pretrained model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token      # GPT-2 has no pad token

model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
model.to(DEVICE)

total_params     = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Params: {total_params:,}")


# ──────────────────────────────────────────────────────────
#  STEP 3 ─ Tokenise & Build HuggingFace Datasets
# ──────────────────────────────────────────────────────────
print("\n[Step 3] Tokenising dataset...")

def tokenise(texts):
    enc = tokenizer(texts, max_length=MAX_LEN, truncation=True,
                    padding="max_length", return_tensors="pt")
    return enc["input_ids"], enc["attention_mask"]

tr_ids, tr_mask = tokenise(train_texts)
vl_ids, vl_mask = tokenise(val_texts)

def make_hf_dataset(ids, mask):
    return Dataset.from_dict({
        "input_ids":      ids.tolist(),
        "attention_mask": mask.tolist(),
        "labels":         ids.tolist(),   # for causal LM labels = input_ids
    })

train_ds = make_hf_dataset(tr_ids, tr_mask)
val_ds   = make_hf_dataset(vl_ids, vl_mask)
collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

print(f"Batches/epoch: {math.ceil(len(train_ds)/BATCH)}")


# ──────────────────────────────────────────────────────────
#  STEP 4 ─ Capture Outputs BEFORE Fine-Tuning
# ──────────────────────────────────────────────────────────
print("\n[Step 4] Generating outputs with BASE model (before fine-tuning)...")

TEST_QS = [
    "What are the admission requirements for undergraduate programs?",
    "How do I access e-journals and online databases?",
    "How do I apply for a fee concession?",
]

def generate(mdl, question, max_new=80):
    prompt  = f"Question: {question}\nAnswer:"
    inputs  = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        out = mdl.generate(
            **inputs,
            max_new_tokens=max_new,
            do_sample=False,
            repetition_penalty=1.3,
            pad_token_id=tokenizer.eos_token_id,
        )
    text = tokenizer.decode(out[0], skip_special_tokens=True)
    return text.split("Answer:", 1)[-1].strip() if "Answer:" in text else text.strip()

pre_outputs = {}
print("\nBefore FT:")
for q in TEST_QS:
    ans = generate(model, q)
    pre_outputs[q] = ans
    print(f"- {q[:45]} → {ans[:80]}...")


# ──────────────────────────────────────────────────────────
#  STEP 5 ─ Fine-Tune (3 Epochs)
# ──────────────────────────────────────────────────────────
print("\n[Step 5] Fine-tuning for 3 epochs ...")

training_args = TrainingArguments(
    output_dir                  = OUTPUT_DIR,
    num_train_epochs            = EPOCHS,
    per_device_train_batch_size = BATCH,
    per_device_eval_batch_size  = BATCH,
    gradient_accumulation_steps = GRAD_ACCUM,
    learning_rate               = LR,
    lr_scheduler_type           = "cosine",
    warmup_steps                = 15,
    weight_decay                = 0.01,
    logging_steps               = 3,
    eval_strategy               = "epoch",
    save_strategy               = "epoch",
    load_best_model_at_end      = True,
    metric_for_best_model       = "eval_loss",
    fp16                        = torch.cuda.is_available(),
    report_to                   = "none",
    seed                        = 42,
)

trainer = Trainer(
    model         = model,
    args          = training_args,
    train_dataset = train_ds,
    eval_dataset  = val_ds,
    data_collator = collator,
)

t0           = time.time()
train_result = trainer.train()
elapsed      = time.time() - t0

print(f"Done. Loss: {train_result.training_loss:.4f}")


# ──────────────────────────────────────────────────────────
#  STEP 6 ─ Extract Metrics from Log History
# ──────────────────────────────────────────────────────────
print("\n[Step 6] Extracting metrics from training log...")

log_history = trainer.state.log_history

train_logs = [(e["step"], e["loss"])
              for e in log_history if "loss" in e and "eval_loss" not in e]
eval_logs  = [(e["epoch"], e["eval_loss"])
              for e in log_history if "eval_loss" in e]

tr_steps  = [x[0] for x in train_logs]
tr_losses = [x[1] for x in train_logs]
ev_epochs = [x[0] for x in eval_logs]
ev_losses = [x[1] for x in eval_logs]
tr_ppls   = [math.exp(l) for l in tr_losses]
ev_ppls   = [math.exp(l) for l in ev_losses]


# ──────────────────────────────────────────────────────────
#  STEP 7 ─ Capture Outputs AFTER Fine-Tuning
# ──────────────────────────────────────────────────────────
print("\n[Step 7] Generating outputs with FINE-TUNED model (after training)...")

post_outputs = {}
print("\nAfter FT:")
for q in TEST_QS:
    ans = generate(model, q)
    post_outputs[q] = ans
    print(f"- {q[:45]} → {ans[:80]}...")


# ──────────────────────────────────────────────────────────
#  STEP 8 ─ Training Loss Graph  →  training_loss_graph.png
# ──────────────────────────────────────────────────────────
print("\n[Step 8] Plotting training loss graph ...")

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(tr_steps, tr_losses, color="#4FC3F7", lw=2, marker="o", ms=4, label="Train Loss")

# Epoch boundary markers
steps_per_epoch = max(1, len(tr_steps) // EPOCHS)
for e in range(1, EPOCHS):
    idx = min(e * steps_per_epoch, len(tr_steps) - 1)
    ax.axvline(x=tr_steps[idx], color="#FFB74D", ls="--", lw=1.2, alpha=0.7,
               label="Epoch boundary" if e == 1 else "_")
    ax.text(tr_steps[idx] + 0.15, max(tr_losses) * 0.97,
            f"Ep {e}", color="#FFB74D", fontsize=9)

ax.set_title(f"Training Loss  –  GPT-2 Fine-Tuned on University FAQ\n"
             f"Epochs: {EPOCHS}  |  LR: {LR}  |  Batch size: {BATCH}", fontsize=12)
ax.set_xlabel("Step")
ax.set_ylabel("Loss")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

graph_path = "training_loss_graph.png"
fig.savefig(graph_path, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"  ✅ Saved → {graph_path}")


# ──────────────────────────────────────────────────────────
#  STEP 9 ─ Output Comparison Table  →  output_comparison.png
# ──────────────────────────────────────────────────────────
print("\n[Step 9] Creating output comparison figure ...")

BG = "#0D1B2A"
WHITE = "#E8EAF0"

WRAP_W = 64     # smaller wrapping width

def wrap(text, width=WRAP_W):
    return "\n".join(textwrap.wrap(text or "(no output)", width))

# Smaller figure
fig2, ax = plt.subplots(figsize=(14, len(TEST_QS) * 2.0 + 1.2), facecolor=BG)

ax.set_facecolor(BG)
ax.axis("off")

# Column layout
COL_X = [0.01, 0.34, 0.67]
COL_W = [0.32, 0.32, 0.32]

HDR_Y = 0.97
ROW_H = 1.0 / (len(TEST_QS) + 2.2)   # smaller rows
PAD   = 0.004                        # less padding

# Header row
headers = ["Question", "Before Fine-Tuning", "After Fine-Tuning"]

hdr_colors = ["#1F3864", "#5C2D00", "#1A3D1A"]
hdr_txt_c  = ["#90CAF9", "#FFB74D", "#81C784"]

for cx, cw, lbl, bg, fc in zip(COL_X, COL_W, headers, hdr_colors, hdr_txt_c):

    fancy = mpatches.FancyBboxPatch(
        (cx, HDR_Y - ROW_H * 0.85), cw - PAD, ROW_H * 0.75,
        boxstyle="round,pad=0.004",
        linewidth=0.8,
        edgecolor=fc,
        facecolor=bg,
        transform=ax.transAxes
    )

    ax.add_patch(fancy)

    ax.text(
        cx + cw/2 - PAD/2,
        HDR_Y - ROW_H * 0.40,
        lbl,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color=fc
    )

# Data rows
cell_bgs  = [["#0F2540", "#2A1500", "#0F2A0F"],
             ["#0A1E35", "#221000", "#0A220A"]]

for i, q in enumerate(TEST_QS):

    y_top = HDR_Y - ROW_H * (i + 1) - ROW_H * 0.02

    texts = [
        wrap(q),
        wrap(pre_outputs.get(q, "")),
        wrap(post_outputs.get(q, "")),
    ]

    txt_colors = ["#B3C8E8", "#FFCC80", "#A5D6A7"]
    cell_bg_row = cell_bgs[i % 2]

    for j, (cx, cw, txt, fc, cbg) in enumerate(
            zip(COL_X, COL_W, texts, txt_colors, cell_bg_row)):

        fancy = mpatches.FancyBboxPatch(
            (cx, y_top - ROW_H * 0.70),
            cw - PAD,
            ROW_H * 0.75,
            boxstyle="round,pad=0.003",
            linewidth=0.5,
            edgecolor="#1E3A5F",
            facecolor=cbg,
            transform=ax.transAxes
        )

        ax.add_patch(fancy)

        text_obj = ax.text(
                cx + 0.006,
                y_top - ROW_H * 0.35,
                txt,
                transform=ax.transAxes,
                ha="left",
                va="center",
                fontsize=6.5,
                color=fc,
                linespacing=1.2,
                clip_on=True
        )

        text_obj.set_clip_path(fancy)

# Title
fig2.suptitle(
    "Output Comparison: Before vs After Fine-Tuning",
    color=WHITE,
    fontsize=11,
    fontweight="bold"
)

compare_path = "output_comparison.png"

fig2.savefig(compare_path, dpi=160, bbox_inches="tight", facecolor=BG)

plt.close(fig2)

print(f"  ✅ Saved → {compare_path}")


# ──────────────────────────────────────────────────────────
#  STEP 9 ─ Save Fine-Tuned Model
# ──────────────────────────────────────────────────────────
print(f"\n[Step 9] Saving fine-tuned model to '{OUTPUT_DIR}' ...")
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"  ✅ Model saved. Reload with:")
print(f"     AutoModelForCausalLM.from_pretrained('{OUTPUT_DIR}')")


# ──────────────────────────────────────────────────────────
#  FINAL SUMMARY
# ──────────────────────────────────────────────────────────
print("\nFinished.")
print(f"Loss: {train_result.training_loss:.4f}")
print(f"Saved: {graph_path}, {compare_path}, {OUTPUT_DIR}")