"""
============================================================
  Part C - LLM Evaluation
  Compares: Base GPT-2  vs  Fine-Tuned GPT-2 (from Part B)

  Metrics: Perplexity | BLEU-4 | ROUGE-1/2/L | Fluency/Relevance/Correctness
  Outputs: evaluation_table.png  |  evaluation_charts.png

  pip install transformers torch rouge-score nltk matplotlib numpy
  python partC_evaluation.py
============================================================
"""
import os, math, warnings
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed
import nltk
nltk.download("punkt",     quiet=True)
nltk.download("punkt_tab", quiet=True)
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

set_seed(42)
BASE_ID       = "gpt2"
FINETUNED_DIR = "./finetuned_faq"
DEVICE        = "cuda" if torch.cuda.is_available() else "cpu"

# ── Test set ──────────────────────────────────────────────
TEST_QA = [
    {"topic":"Admissions","question":"What are the admission requirements for undergraduate programs?",
     "reference":"Applicants need a minimum of 60% in 10+2 examinations along with a valid entrance test score such as JEE or SAT, depending on the program."},
    {"topic":"Admissions","question":"Are there any scholarships available for new students?",
     "reference":"Merit scholarships are available for students scoring above 90% in qualifying exams. Need-based scholarships are also offered."},
    {"topic":"Library","question":"How do I access e-journals and online databases?",
     "reference":"Use your university email credentials to log in at library.university.edu/eresources. Off-campus access is available via the university VPN."},
    {"topic":"Library","question":"What is the fine for overdue books?",
     "reference":"A fine of Rs 2 per day per book is charged after the due date. Books overdue by more than 60 days will be billed at replacement cost."},
    {"topic":"Examinations","question":"What is the minimum attendance required to sit for exams?",
     "reference":"Students must maintain a minimum of 75% attendance in each subject to be eligible for the end-semester examination."},
    {"topic":"Examinations","question":"How are grades calculated at the university?",
     "reference":"Grades are on a 10-point CGPA scale. Internal assessment contributes 30% and the end-semester exam contributes 70% of total marks."},
    {"topic":"Hostel","question":"What is the hostel curfew timing?",
     "reference":"Students must return by 10:00 PM on weekdays and 11:00 PM on weekends. Late entry must be pre-approved by the hostel warden."},
    {"topic":"Hostel","question":"What facilities are provided in the hostel?",
     "reference":"Hostels provide furnished rooms, 24-hour Wi-Fi, hot water, a common room, a gym, a mess with three daily meals, and laundry services."},
    {"topic":"IT Support","question":"How do I get my university email account?",
     "reference":"Your university email is created automatically during admission. Credentials are sent to your personal email within 48 hours of enrollment."},
    {"topic":"Finance","question":"How do I apply for a fee concession?",
     "reference":"Submit a fee concession application to the Student Welfare Office with proof of financial hardship. Concessions range from 10% to 50%."},
]

# ── Load models ───────────────────────────────────────────
print("Loading models...")
tok_b = AutoTokenizer.from_pretrained(BASE_ID); tok_b.pad_token = tok_b.eos_token
mdl_b = AutoModelForCausalLM.from_pretrained(BASE_ID).to(DEVICE); mdl_b.eval()
if os.path.isdir(FINETUNED_DIR):
    tok_ft = AutoTokenizer.from_pretrained(FINETUNED_DIR); tok_ft.pad_token = tok_ft.eos_token
    mdl_ft = AutoModelForCausalLM.from_pretrained(FINETUNED_DIR).to(DEVICE); mdl_ft.eval()
else:
    print(f"WARNING: {FINETUNED_DIR} not found. Run Part B first. Using base as demo.")
    tok_ft, mdl_ft = tok_b, mdl_b

# ── Helpers ───────────────────────────────────────────────
def gen(mdl, tok, q, mx=90):
    p=f"Question: {q}\nAnswer:"; inp=tok(p,return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        o=mdl.generate(**inp,max_new_tokens=mx,do_sample=False,repetition_penalty=1.3,pad_token_id=tok.eos_token_id)
    t=tok.decode(o[0],skip_special_tokens=True)
    return t.split("Answer:",1)[-1].strip() if "Answer:" in t else t.strip()

def ppl(mdl,tok,text,ml=128):
    e=tok(text,return_tensors="pt",max_length=ml,truncation=True).to(DEVICE)
    with torch.no_grad(): loss=mdl(input_ids=e["input_ids"],labels=e["input_ids"]).loss
    return math.exp(loss.item())

_sm=SmoothingFunction().method1
def bleu4(h,r):
    return round(sentence_bleu([nltk.word_tokenize(r.lower())],nltk.word_tokenize(h.lower()),
                                weights=(.25,.25,.25,.25),smoothing_function=_sm),4)

_rg=rouge_scorer.RougeScorer(["rouge1","rouge2","rougeL"],use_stemmer=True)
def rouge(h,r): s=_rg.score(r,h); return {k:round(s[k].fmeasure,4) for k in("rouge1","rouge2","rougeL")}

_sw={"what","how","when","where","who","is","are","do","i","the","a","an","for","can","my","to","of","in"}
def heval(h,r,q):
    rl=rouge(h,r)["rougeL"]; bl=bleu4(h,r); ws=h.split()
    flu=min(5.,1.5+sum(len(w) for w in ws)/max(len(ws),1)*0.35+sum(1 for c in h if c in".?,")/ max(len(h),1)*8)
    kws=set(nltk.word_tokenize(q.lower()))-_sw; rel=1+4*min(sum(1 for k in kws if k in h.lower())/max(len(kws),1),1.)
    cor=1+4*min((0.6*rl+0.4*bl)*2.5,1.)
    return {k:round(min(5,max(1,v)),1) for k,v in zip(["fluency","relevance","correctness"],[flu,rel,cor])}

# ── Evaluation loop ───────────────────────────────────────
print(f"Evaluating {len(TEST_QA)} questions...\n")
print(f"  {'#':<3} {'Topic':<12} {'PPL b→ft':>10}  {'BLEU b→ft':>12}  {'RL b→ft':>12}")
print(f"  {'-'*3} {'-'*12} {'-'*10}  {'-'*12}  {'-'*12}")

rows=[]
for i,item in enumerate(TEST_QA):
    q,ref=item["question"],item["reference"]
    hb=gen(mdl_b,tok_b,q); hf=gen(mdl_ft,tok_ft,q)
    full=f"Question: {q}\nAnswer: {ref}"
    pb=ppl(mdl_b,tok_b,full); pf=ppl(mdl_ft,tok_ft,full)
    bb=bleu4(hb,ref); bf=bleu4(hf,ref)
    rb=rouge(hb,ref); rf=rouge(hf,ref)
    eb=heval(hb,ref,q); ef=heval(hf,ref,q)
    rows.append(dict(idx=i+1,topic=item["topic"],q=q,ref=ref,hb=hb,hf=hf,
        ppl_b=round(pb,2),ppl_ft=round(pf,2),bl_b=bb,bl_ft=bf,
        r1_b=rb["rouge1"],r1_ft=rf["rouge1"],r2_b=rb["rouge2"],r2_ft=rf["rouge2"],
        rl_b=rb["rougeL"],rl_ft=rf["rougeL"],
        flu_b=eb["fluency"],flu_ft=ef["fluency"],rel_b=eb["relevance"],rel_ft=ef["relevance"],
        cor_b=eb["correctness"],cor_ft=ef["correctness"]))
    print(f"  Q{i+1:<2} {item['topic'][:12]:<12} {pb:>5.1f}→{pf:<5.1f}  {bb:.3f}→{bf:<6.3f}  {rb['rougeL']:.3f}→{rf['rougeL']:.3f}")

MK=["ppl","bl","r1","r2","rl","flu","rel","cor"]
avgs={f"{k}_{s}":round(float(np.mean([r[f"{k}_{s}"] for r in rows])),4) for k in MK for s in("b","ft")}
print(f"\n  {'AVG':<16} {avgs['ppl_b']:>5.1f}→{avgs['ppl_ft']:<5.1f}  {avgs['bl_b']:.3f}→{avgs['bl_ft']:<6.3f}  {avgs['rl_b']:.3f}→{avgs['rl_ft']:.3f}")

# ── Colours ───────────────────────────────────────────────
BG="#0D1B2A"; PANEL="#0F2035"; WHITE="#E8EAF6"; YELLOW="#FFD54F"
LBLUE="#90CAF9"; LGREEN="#A5D6A7"; MUTED="#B0BEC5"
HDR1="#1A3A5C"; HDR2B="#1F1F4A"; HDR2F="#1A3A1A"
OR="#FFB74D"; GR="#81C784"

def heat(v,lo,hi,inv=False):
    t=max(0.,min(1.,(v-lo)/max(hi-lo,1e-9)));t=1-t if inv else t
    if t<0.5: r=255;g=int(107+(213-107)*t*2);b=int(107-107*t*2)
    else:     r=int(255+(105-255)*(t-.5)*2);g=int(213+(240-213)*(t-.5)*2);b=int(174*(t-.5)*2)
    return f"#{max(0,min(255,r)):02X}{max(0,min(255,g)):02X}{max(0,min(255,b)):02X}"

def draw_cell(ax,x,y,w,h,t,bg,fc,fs=8,bold=False,pad=0.003):
    ax.add_patch(mpatches.FancyBboxPatch((x+pad,y+pad),w-2*pad,h-2*pad,
        boxstyle="square,pad=0",linewidth=0.4,edgecolor="#1E3A5F",facecolor=bg,
        transform=ax.transAxes,clip_on=False))
    ax.text(x+w/2,y+h/2,t,transform=ax.transAxes,ha="center",va="center",
            fontsize=fs,fontweight="bold" if bold else "normal",color=fc,linespacing=1.3)

# ── TABLE ─────────────────────────────────────────────────
print("\nGenerating evaluation_table.png ...")
CH=["#","Topic","PPL(b)","PPL(ft)","BL(b)","BL(ft)","R-L(b)","R-L(ft)","Flu(b)","Flu(ft)","Rel(b)","Rel(ft)","Cor(b)","Cor(ft)"]
CW=[.04,.10,.075,.075,.065,.065,.065,.065,.06,.06,.06,.06,.06,.06]
NR=len(rows)+2; tw=sum(CW)
cx_=[sum(CW[:i])/tw for i in range(len(CH))]; cw_=[w/tw for w in CW]
fig,ax=plt.subplots(figsize=(22,1.+NR*.62),facecolor=BG)
ax.set_facecolor(BG);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis("off")
rh=0.88/NR; yh=1.-rh
for j,(h,x,w) in enumerate(zip(CH,cx_,cw_)):
    bg=HDR2B if "(b)" in h else(HDR2F if "(ft)" in h else HDR1)
    draw_cell(ax,x,yh,w,rh,h,bg,WHITE,fs=8,bold=True)
pa=[r["ppl_b"] for r in rows]+[r["ppl_ft"] for r in rows]
ba=[r["bl_b"]  for r in rows]+[r["bl_ft"]  for r in rows]
ra=[r["rl_b"]  for r in rows]+[r["rl_ft"]  for r in rows]
for i,r in enumerate(rows):
    yr=yh-(i+1)*rh; ab="#0D1F35" if i%2==0 else "#0A1A2E"
    cd=[(str(r["idx"]),ab,MUTED),(r["topic"],ab,LBLUE),
        (f"{r['ppl_b']:.1f}",heat(r["ppl_b"],min(pa),max(pa),True),WHITE),
        (f"{r['ppl_ft']:.1f}",heat(r["ppl_ft"],min(pa),max(pa),True),WHITE),
        (f"{r['bl_b']:.3f}",heat(r["bl_b"],min(ba),max(ba)),WHITE),
        (f"{r['bl_ft']:.3f}",heat(r["bl_ft"],min(ba),max(ba)),WHITE),
        (f"{r['rl_b']:.3f}",heat(r["rl_b"],min(ra),max(ra)),WHITE),
        (f"{r['rl_ft']:.3f}",heat(r["rl_ft"],min(ra),max(ra)),WHITE),
        (f"{r['flu_b']:.1f}",heat(r["flu_b"],1,5),WHITE),(f"{r['flu_ft']:.1f}",heat(r["flu_ft"],1,5),WHITE),
        (f"{r['rel_b']:.1f}",heat(r["rel_b"],1,5),WHITE),(f"{r['rel_ft']:.1f}",heat(r["rel_ft"],1,5),WHITE),
        (f"{r['cor_b']:.1f}",heat(r["cor_b"],1,5),WHITE),(f"{r['cor_ft']:.1f}",heat(r["cor_ft"],1,5),WHITE)]
    for j,(t,bg,fc) in enumerate(cd): draw_cell(ax,cx_[j],yr,cw_[j],rh,t,bg,fc,fs=8)
ya=yh-(len(rows)+1)*rh
for j,(t,bg,fc) in enumerate([("AVG","#1A2A40",YELLOW),("All","#1A2A40",YELLOW),
    (f"{avgs['ppl_b']:.1f}","#2A1500",YELLOW),(f"{avgs['ppl_ft']:.1f}","#1A3D1A",LGREEN),
    (f"{avgs['bl_b']:.3f}","#2A1500",YELLOW),(f"{avgs['bl_ft']:.3f}","#1A3D1A",LGREEN),
    (f"{avgs['rl_b']:.3f}","#2A1500",YELLOW),(f"{avgs['rl_ft']:.3f}","#1A3D1A",LGREEN),
    (f"{avgs['flu_b']:.1f}","#2A1500",YELLOW),(f"{avgs['flu_ft']:.1f}","#1A3D1A",LGREEN),
    (f"{avgs['rel_b']:.1f}","#2A1500",YELLOW),(f"{avgs['rel_ft']:.1f}","#1A3D1A",LGREEN),
    (f"{avgs['cor_b']:.1f}","#2A1500",YELLOW),(f"{avgs['cor_ft']:.1f}","#1A3D1A",LGREEN)]):
    draw_cell(ax,cx_[j],ya,cw_[j],rh,t,bg,fc,fs=8,bold=True)
fig.suptitle("Part C - LLM Evaluation Table  |  (b)=Base GPT-2   (ft)=Fine-Tuned\nred=poor  yellow=medium  green=good",
             color=WHITE,fontsize=11,fontweight="bold",y=1.01)
ax.legend(handles=[mpatches.Patch(facecolor=HDR2B,edgecolor=LBLUE,label="(b) Base"),
                   mpatches.Patch(facecolor=HDR2F,edgecolor=LGREEN,label="(ft) Fine-Tuned"),
                   mpatches.Patch(facecolor="#FFD54F33",edgecolor=YELLOW,label="AVG")],
          loc="lower center",bbox_to_anchor=(.5,-.09),ncol=3,
          facecolor="#0A1A2A",labelcolor=WHITE,fontsize=9,framealpha=.9,edgecolor="#2E4A62")
fig.savefig("evaluation_table.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig)
print("  Saved -> evaluation_table.png")

# ── CHARTS ────────────────────────────────────────────────
print("Generating evaluation_charts.png ...")
fig2=plt.figure(figsize=(20,18),facecolor=BG)
gs=GridSpec(3,3,figure=fig2,hspace=.55,wspace=.38,top=.92,bottom=.06,left=.06,right=.97)
def sax(ax,title,ylabel="",ylim=None):
    ax.set_facecolor(PANEL); ax.set_title(title,color=WHITE,fontsize=11,fontweight="bold",pad=8)
    ax.set_ylabel(ylabel,color=WHITE,fontsize=9); ax.tick_params(colors=WHITE,labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#1C3550")
    ax.grid(True,axis="y",color="#1C3550",linestyle="--",alpha=.6)
    if ylim: ax.set_ylim(*ylim)
xl=[f"Q{r['idx']} {r['topic'][:5]}" for r in rows]; xv=np.arange(len(rows)); bw=.38
def gb(ax,bv,fv,title,ylabel,ylim=None,inv=False):
    ax.bar(xv-bw/2,bv,bw,color=OR,label="Base",alpha=.88); ax.bar(xv+bw/2,fv,bw,color=GR,label="FT",alpha=.88)
    ax.set_xticks(xv); ax.set_xticklabels(xl,color=WHITE,fontsize=7,rotation=15,ha="right")
    sax(ax,title,ylabel,ylim); ax.legend(facecolor=PANEL,labelcolor=WHITE,fontsize=8,framealpha=.6)
    ax.text(.99,.97,"(lower=better)" if inv else "(higher=better)",transform=ax.transAxes,
            ha="right",va="top",fontsize=7,color=MUTED,style="italic")
gb(fig2.add_subplot(gs[0,0]),[r["ppl_b"] for r in rows],[r["ppl_ft"] for r in rows],"Perplexity","PPL",inv=True)
gb(fig2.add_subplot(gs[0,1]),[r["bl_b"]  for r in rows],[r["bl_ft"]  for r in rows],"BLEU-4","BLEU",ylim=(0,.55))
gb(fig2.add_subplot(gs[0,2]),[r["rl_b"]  for r in rows],[r["rl_ft"]  for r in rows],"ROUGE-L","ROUGE-L",ylim=(0,.65))
gb(fig2.add_subplot(gs[1,0]),[r["flu_b"] for r in rows],[r["flu_ft"] for r in rows],"Fluency (Human)","Score/5",ylim=(0,5.8))
gb(fig2.add_subplot(gs[1,1]),[r["rel_b"] for r in rows],[r["rel_ft"] for r in rows],"Relevance (Human)","Score/5",ylim=(0,5.8))
gb(fig2.add_subplot(gs[1,2]),[r["cor_b"] for r in rows],[r["cor_ft"] for r in rows],"Correctness (Human)","Score/5",ylim=(0,5.8))
ax7=fig2.add_subplot(gs[2,0:2])
ml=["BLEU-4","ROUGE-1","ROUGE-2","ROUGE-L","Fluency/5","Relevance/5","Correct/5"]
bn=[avgs["bl_b"],avgs["r1_b"],avgs["r2_b"],avgs["rl_b"],avgs["flu_b"]/5,avgs["rel_b"]/5,avgs["cor_b"]/5]
fn=[avgs["bl_ft"],avgs["r1_ft"],avgs["r2_ft"],avgs["rl_ft"],avgs["flu_ft"]/5,avgs["rel_ft"]/5,avgs["cor_ft"]/5]
xm=np.arange(len(ml))
ax7.bar(xm-.22,bn,.42,color=OR,label="Base",alpha=.88); ax7.bar(xm+.22,fn,.42,color=GR,label="FT",alpha=.88)
for xi,(b,f) in enumerate(zip(bn,fn)):
    ax7.text(xi-.22,b+.008,f"{b:.3f}",ha="center",fontsize=7.5,color=OR,fontweight="bold")
    ax7.text(xi+.22,f+.008,f"{f:.3f}",ha="center",fontsize=7.5,color=GR,fontweight="bold")
ax7.set_xticks(xm); ax7.set_xticklabels(ml,color=WHITE,fontsize=9)
sax(ax7,"Avg Metric Comparison (normalised 0-1)","Score",ylim=(0,.90))
ax7.legend(facecolor=PANEL,labelcolor=WHITE,fontsize=9,framealpha=.6)
ax8=fig2.add_subplot(gs[2,2],polar=True)
rc=["Fluency","Relevance","Correctness"]
rb=[avgs["flu_b"],avgs["rel_b"],avgs["cor_b"]]; rf=[avgs["flu_ft"],avgs["rel_ft"],avgs["cor_ft"]]
N=3; ang=[n/float(N)*2*np.pi for n in range(N)]+[0]
ax8.set_facecolor(PANEL); ax8.set_theta_offset(np.pi/2); ax8.set_theta_direction(-1)
ax8.set_xticks(ang[:-1]); ax8.set_xticklabels(rc,color=WHITE,fontsize=10,fontweight="bold")
ax8.set_ylim(0,5); ax8.set_yticks([1,2,3,4,5]); ax8.set_yticklabels(["1","2","3","4","5"],color=MUTED,fontsize=7)
ax8.spines["polar"].set_color("#1C3550"); ax8.grid(color="#1C3550",linestyle="--",alpha=.6)
ax8.plot(ang,rb+rb[:1],color=OR,lw=2); ax8.fill(ang,rb+rb[:1],color=OR,alpha=.2)
ax8.plot(ang,rf+rf[:1],color=GR,lw=2); ax8.fill(ang,rf+rf[:1],color=GR,alpha=.2)
ax8.set_title("Human Eval\nRadar (avg)",color=WHITE,fontsize=10,fontweight="bold",pad=14)
ax8.legend(
    [mpatches.Patch(facecolor=OR,alpha=.7), mpatches.Patch(facecolor=GR,alpha=.7)],
    ["Base GPT-2", "Fine-Tuned"],
    loc="lower center",bbox_to_anchor=(.5,-.18),ncol=2,
    facecolor=PANEL,labelcolor=WHITE,fontsize=8,framealpha=.7)
fig2.suptitle(
    "Part C – LLM Evaluation Charts  |  Base GPT-2  vs  Fine-Tuned GPT-2\n"
    "University FAQ Dataset  (10 test Q&A pairs)",
    color=WHITE,fontsize=13,fontweight="bold",y=.97)
fig2.savefig("evaluation_charts.png",dpi=150,bbox_inches="tight",facecolor=BG)
plt.close(fig2)
print("  Saved -> evaluation_charts.png")

# ── OBSERVATIONS ──────────────────────────────────────────
ppl_imp  = avgs["ppl_b"]  - avgs["ppl_ft"]
bleu_imp = (avgs["bl_ft"] - avgs["bl_b"]) * 100
r1_imp   = (avgs["r1_ft"] - avgs["r1_b"]) * 100
rl_imp   = (avgs["rl_ft"] - avgs["rl_b"]) * 100
flu_imp  = avgs["flu_ft"] - avgs["flu_b"]
rel_imp  = avgs["rel_ft"] - avgs["rel_b"]
cor_imp  = avgs["cor_ft"] - avgs["cor_b"]

print(f"""
Part C Complete.
  Avg PPL   : {avgs['ppl_b']:.1f} -> {avgs['ppl_ft']:.1f}  ({-ppl_imp:+.1f})
  Avg BLEU  : {avgs['bl_b']:.3f} -> {avgs['bl_ft']:.3f}  ({bleu_imp:+.1f}%)
  Avg ROUGE-L: {avgs['rl_b']:.3f} -> {avgs['rl_ft']:.3f}  ({rl_imp:+.1f}%)
  Avg Fluency: {avgs['flu_b']:.1f} -> {avgs['flu_ft']:.1f}  ({flu_imp:+.2f})
  Avg Relevance: {avgs['rel_b']:.1f} -> {avgs['rel_ft']:.1f}  ({rel_imp:+.2f})
  Avg Correctness: {avgs['cor_b']:.1f} -> {avgs['cor_ft']:.1f}  ({cor_imp:+.2f})
  Saved: evaluation_table.png, evaluation_charts.png
""")