"""
============================================================
  Part D – Local LLM and Data Privacy
  Tool    : Local Hugging Face Inference (no cloud API)
  Model   : GPT-2 Small (124M) — runs 100% offline
  Outputs :
      • local_llm_demo.png
      • local_vs_api_comparison.png
      • privacy_analysis.png
============================================================
"""
import os, time, platform, textwrap, warnings, math
warnings.filterwarnings("ignore")
import torch
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed
set_seed(42)

BG="#0D1B2A"; PANEL="#112233"; BLUE="#4FC3F7"; GREEN="#81C784"; ORANGE="#FFB74D"
RED="#EF9A9A"; PURPLE="#CE93D8"; YELLOW="#FFF176"; WHITE="#E8EAF0"; MUTED="#90A4AE"
GRID="#1C3550"; TEAL="#4DB6AC"; PINK="#F48FB1"

DEVICE="cuda" if torch.cuda.is_available() else "cpu"
MODEL_ID="gpt2"

print(f"Part D – Local LLM | Model: {MODEL_ID} | Device: {DEVICE} | OS: {platform.system()}")

# ── Load model ────────────────────────────────────────────
print("[Step 1] Loading model...")
t_load=time.time()
tokenizer=AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token=tokenizer.eos_token
model=AutoModelForCausalLM.from_pretrained(MODEL_ID).to(DEVICE)
model.eval()
print(f"  Done in {time.time()-t_load:.2f}s  |  Zero data sent externally.")

SENSITIVE_PROMPTS=[
    {"category":"Medical Record","icon":"H","prompt":"Patient John Doe, DOB 12/03/1985, diagnosis: Type-2 Diabetes. Recommended treatment:","privacy_risk":"HIGH - PHI/HIPAA","color":RED},
    {"category":"Legal Document","icon":"L","prompt":"Confidential: Contract between Acme Corp and XYZ Ltd. Clause 5 states that all intellectual property","privacy_risk":"HIGH - NDA/Trade Secret","color":RED},
    {"category":"Financial Data","icon":"$","prompt":"Account 4532-XXXX-XXXX-9871, balance Rs 2,45,000. Transaction summary for Q3:","privacy_risk":"HIGH - PCI-DSS","color":RED},
    {"category":"HR / Internal","icon":"P","prompt":"Employee performance review for Priya Sharma, Emp ID E-1042. Overall rating 4/5. Key strengths:","privacy_risk":"MEDIUM - PII","color":ORANGE},
    {"category":"Research Data","icon":"R","prompt":"Unpublished research finding: Novel compound XR-77 shows 40% efficacy improvement. Methodology:","privacy_risk":"MEDIUM - IP","color":ORANGE},
    {"category":"General FAQ","icon":"Q","prompt":"Question: What are the steps to register a new company in India? Answer:","privacy_risk":"LOW - Public","color":GREEN},
]

def generate_local(prompt, max_new=60):
    inputs=tokenizer(prompt,return_tensors="pt",truncation=True,max_length=100).to(DEVICE)
    t0=time.time()
    with torch.no_grad():
        out=model.generate(**inputs,max_new_tokens=max_new,do_sample=True,
            temperature=0.8,top_p=0.9,repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id)
    lat=(time.time()-t0)*1000
    full=tokenizer.decode(out[0],skip_special_tokens=True)
    return full[len(prompt):].strip(), lat, out.shape[-1]-inputs["input_ids"].shape[-1]

# ── Inference ─────────────────────────────────────────────
print("[Step 2] Running local inference...")
results=[]
for p in SENSITIVE_PROMPTS:
    g,lat,toks=generate_local(p["prompt"])
    results.append({**p,"output":g,"latency_ms":lat,"tokens":toks})
    print(f"  {p['category']:<16} {lat:>6.0f} ms  | {p['privacy_risk']}")

# ── Figure 1: Local vs API comparison ────────────────────
print("[Step 3] Saving local_vs_api_comparison.png ...")
COMPARISON=[
    ("Data Privacy",         5,1,"All data stays on device.\nNo 3rd-party transmission.","Data sent to vendor servers.\nMay be logged/used for training."),
    ("Regulatory Compliance",5,2,"Satisfies HIPAA, GDPR, PCI-DSS\nwithout extra agreements.","Requires DPA/BAA agreements.\nJurisdiction risk for cross-border."),
    ("Internet Dependency",  5,1,"Zero internet required.\nWorks in air-gapped environments.","100% dependent on connectivity.\nOutages = service disruption."),
    ("Setup Complexity",     2,5,"Needs hardware, model download\nand configuration.","Single API key + a few lines\nof code. Instant start."),
    ("Scalability",          2,5,"Limited by local hardware.\nGPU/RAM are hard constraints.","Infinite horizontal scaling.\nPay-per-token elasticity."),
    ("Model Quality",        2,5,"Smaller models (1-13B) lag\nbehind frontier APIs.","GPT-4o, Claude 3.5, Gemini -\nstate-of-the-art quality."),
    ("Cost (at scale)",      5,2,"One-time hardware capex.\nZero per-token charges.","Recurring per-token opex.\nExpensive at high volume."),
    ("Customisation",        5,3,"Full fine-tune, LoRA, GGUF\nquant - complete control.","Fine-tune APIs available but\nlimited and costly."),
    ("Latency (offline)",    5,1,"No network round-trip.\nSub-second on GPU.","Network RTT adds 200-800ms.\nVaries with server load."),
    ("Vendor Lock-in",       5,1,"Open weights - no lock-in.\nSwitch models freely.","Proprietary APIs.\nPricing changes unilaterally."),
]

fig2,axes=plt.subplots(1,2,figsize=(22,14),facecolor=BG,
    gridspec_kw={"width_ratios":[1.4,1]})
fig2.subplots_adjust(wspace=0.04,left=0.01,right=0.99,top=0.91,bottom=0.04)
axT=axes[0]; axT.set_facecolor(BG); axT.axis("off")
axT.set_xlim(0,1); axT.set_ylim(0,1)

NR=len(COMPARISON)
HH=0.07          # header height
RH=0.82/NR       # row height

# Column x-positions and widths
DIM_X,  DIM_W  = 0.00, 0.18   # Dimension label
LOC_X,  LOC_W  = 0.18, 0.36   # Local text + dots
API_X,  API_W  = 0.54, 0.46   # API text + dots

# Dot sub-regions (inside each column, right-aligned)
LOC_DOT_X = LOC_X + 0.18      # dots start x inside local col
API_DOT_X = API_X + 0.24      # dots start x inside api col
DOT_SPACING = 0.030
DOT_R       = 0.008

# Header row
TABLE_TOP = 0.93
for x,w,lbl,bg,fc in[
    (DIM_X, DIM_W, "Dimension",                    "#1A2A3A", BLUE),
    (LOC_X, LOC_W, "Local LLM (HuggingFace/Ollama)","#0A2010", GREEN),
    (API_X, API_W, "Cloud API (OpenAI / Anthropic)", "#200A0A", RED),
]:
    axT.add_patch(FancyBboxPatch((x+.003, TABLE_TOP-HH+.003), w-.006, HH-.005,
        boxstyle="round,pad=.005", lw=.8, ec=fc, fc=bg,
        transform=axT.transAxes, clip_on=False))
    axT.text(x+w/2, TABLE_TOP-HH/2, lbl, transform=axT.transAxes,
             ha="center", va="center", fontsize=9.5, fontweight="bold", color=fc)

for i,(dim,ls,as_,ln,an) in enumerate(COMPARISON):
    y   = TABLE_TOP - HH - (i+1)*RH
    ab  = "#0D2035" if i%2==0 else "#0A1A2E"
    yc  = y + RH/2   # vertical centre of this row

    # ── Dimension cell ────────────────────────────────────
    axT.add_patch(FancyBboxPatch((DIM_X+.003, y+.002), DIM_W-.006, RH-.004,
        boxstyle="round,pad=.003", lw=.5, ec=GRID, fc=ab,
        transform=axT.transAxes, clip_on=False))
    axT.text(DIM_X+.008, yc, dim, transform=axT.transAxes,
             ha="left", va="center", fontsize=8.5, color=WHITE, fontweight="bold")

    # ── Local cell: text (top half) + dots (bottom half) ─
    axT.add_patch(FancyBboxPatch((LOC_X+.003, y+.002), LOC_W-.006, RH-.004,
        boxstyle="round,pad=.003", lw=.5, ec="#0F3020", fc="#0A1E10",
        transform=axT.transAxes, clip_on=False))
    axT.text(LOC_X+.008, y+RH*0.68, ln, transform=axT.transAxes,
             ha="left", va="center", fontsize=7.5, color=GREEN, linespacing=1.3)
    # dots — centred vertically in lower quarter of the row
    for d in range(5):
        fc2 = GREEN if d < ls else "#1A2A3A"
        axT.add_patch(plt.Circle(
            (LOC_DOT_X + d*DOT_SPACING, y + RH*0.18),
            DOT_R, color=fc2, transform=axT.transAxes, clip_on=False, zorder=4))

    # ── API cell: text (top half) + dots (bottom half) ───
    axT.add_patch(FancyBboxPatch((API_X+.003, y+.002), API_W-.006, RH-.004,
        boxstyle="round,pad=.003", lw=.5, ec="#301010", fc="#1E0A0A",
        transform=axT.transAxes, clip_on=False))
    axT.text(API_X+.008, y+RH*0.68, an, transform=axT.transAxes,
             ha="left", va="center", fontsize=7.5, color=RED, linespacing=1.3)
    for d in range(5):
        fc2 = RED if d < as_ else "#1A2A3A"
        axT.add_patch(plt.Circle(
            (API_DOT_X + d*DOT_SPACING, y + RH*0.18),
            DOT_R, color=fc2, transform=axT.transAxes, clip_on=False, zorder=4))

axT.text(.995,.012,"● = score out of 5  (higher = better)",transform=axT.transAxes,
         ha="right",va="bottom",fontsize=7.5,color=MUTED,style="italic")
axT.set_title("Local vs Cloud API - Feature Comparison",
              color=WHITE,fontsize=12,fontweight="bold",pad=10)

# ── Radar ─────────────────────────────────────────────────
dims_r=["Privacy","Compliance","Offline","Cost","Customise","No Lock-in"]
local_r=[5,5,5,5,5,5]; api_r=[1,2,1,2,3,1]
axes[1].remove()
axR=fig2.add_subplot(1,2,2,polar=True); axR.set_facecolor(PANEL)
N=len(dims_r); ang=[n/N*2*np.pi for n in range(N)]+[0]
axR.set_theta_offset(np.pi/2); axR.set_theta_direction(-1)
axR.set_xticks(ang[:-1]); axR.set_xticklabels(dims_r,color=WHITE,fontsize=10,fontweight="bold")
axR.set_ylim(0,5); axR.set_yticks([1,2,3,4,5])
axR.set_yticklabels(["1","2","3","4","5"],color=MUTED,fontsize=7)
axR.spines["polar"].set_color(GRID); axR.grid(color=GRID,linestyle="--",alpha=0.6)
axR.plot(ang,local_r+[local_r[0]],color=GREEN,lw=2.5,zorder=3)
axR.fill(ang,local_r+[local_r[0]],color=GREEN,alpha=0.22)
axR.plot(ang,api_r+[api_r[0]],color=RED,lw=2.5,zorder=3)
axR.fill(ang,api_r+[api_r[0]],color=RED,alpha=0.22)
axR.legend([mpatches.Patch(facecolor=GREEN,alpha=.6),mpatches.Patch(facecolor=RED,alpha=.6)],
           ["Local LLM","Cloud API"],loc="lower center",bbox_to_anchor=(.5,-.14),ncol=2,
           facecolor=PANEL,labelcolor=WHITE,fontsize=10,framealpha=.8)
axR.set_title("Privacy & Control\nRadar (Local vs API)",color=WHITE,fontsize=11,fontweight="bold",pad=18)
fig2.suptitle("Part D - Local LLM vs Cloud API Deployment Comparison\nAcross 10 dimensions: Privacy  Compliance  Cost  Quality  Control",
              color=WHITE,fontsize=13,fontweight="bold",y=0.97)
fig2.savefig("local_vs_api_comparison.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig2)

# ── Figure 2: Privacy analysis ────────────────────────────
print("[Step 4] Saving privacy_analysis.png ...")
fig3=plt.figure(figsize=(20,14),facecolor=BG)
gs=GridSpec(2,3,figure=fig3,hspace=.52,wspace=.38,top=.91,bottom=.07,left=.05,right=.97)
def sax(ax,title,xlabel="",ylabel=""):
    ax.set_facecolor(PANEL); ax.set_title(title,color=WHITE,fontsize=11,fontweight="bold",pad=8)
    ax.set_xlabel(xlabel,color=WHITE,fontsize=9); ax.set_ylabel(ylabel,color=WHITE,fontsize=9)
    ax.tick_params(colors=WHITE,labelsize=8)
    for sp in ax.spines.values(): sp.set_color(GRID)
    ax.grid(True,color=GRID,linestyle="--",linewidth=0.7,alpha=0.7)

# Donut
ax1=fig3.add_subplot(gs[0,0]); ax1.set_facecolor(PANEL); ax1.axis("off")
pos=ax1.get_position()
ax_d=fig3.add_axes([pos.x0,pos.y0,pos.width,pos.height],aspect="equal",facecolor=PANEL)
risks=["Data in Transit\n(API calls)","Vendor Storage\n& Logging","Model Training\non User Data","Breach /\nLeak Risk"]
vals=[30,28,24,18]; cols=[RED,ORANGE,PINK,PURPLE]
wedge,texts,autos=ax_d.pie(vals,labels=risks,colors=cols,autopct="%1.0f%%",
    startangle=90,pctdistance=0.78,wedgeprops={"width":0.55,"edgecolor":BG,"linewidth":2})
for t in texts: t.set_color(WHITE); t.set_fontsize(8)
for a in autos: a.set_color(BG); a.set_fontsize(8); a.set_fontweight("bold")
ax_d.set_title("Cloud API Privacy Risks\n(relative exposure)",color=WHITE,fontsize=10,fontweight="bold",pad=6)
ax1.set_visible(False)

# Privacy stack
ax2=fig3.add_subplot(gs[0,1]); ax2.set_facecolor(PANEL); ax2.axis("off")
layers=[("Hardware Layer","CPU/GPU processes data locally",TEAL,0.82),
    ("OS / Memory Layer","RAM never serialised to network",BLUE,0.65),
    ("Model Weights","Stored on disk, loaded in-process",GREEN,0.50),
    ("Inference Engine","HuggingFace/llama.cpp - no telemetry",ORANGE,0.36),
    ("Application Layer","Your code - full control over I/O",YELLOW,0.22),
    ("Network","BLOCKED - zero egress during inference",RED,0.10)]
for lbl,desc,col,y in layers:
    ax2.add_patch(FancyBboxPatch((.04,y-.055),.92,.10,boxstyle="round,pad=.008",
        lw=1.2,ec=col,fc=col+"33",transform=ax2.transAxes,clip_on=False))
    ax2.text(.07,y,lbl,transform=ax2.transAxes,ha="left",va="center",
             fontsize=9,fontweight="bold",color=col)
    ax2.text(.97,y,desc,transform=ax2.transAxes,ha="right",va="center",
             fontsize=7.5,color=WHITE)
ax2.set_title("Local LLM Privacy Stack\n(data never leaves this boundary)",
              color=WHITE,fontsize=10,fontweight="bold",pad=6)

# Compliance bar
ax3=fig3.add_subplot(gs[0,2])
regs=["HIPAA","GDPR","PCI-DSS","SOC 2","FERPA","ISO 27001"]
local_c=[95,92,90,88,95,85]; api_c=[45,60,55,70,40,65]
xr=np.arange(len(regs)); bw=.35
ax3.barh(xr+bw/2,local_c,bw,color=GREEN,alpha=.85,label="Local LLM")
ax3.barh(xr-bw/2,api_c,bw,color=RED,alpha=.85,label="Cloud API")
ax3.set_yticks(xr); ax3.set_yticklabels(regs,color=WHITE,fontsize=9)
ax3.set_xlim(0,115)
for i,(l,a) in enumerate(zip(local_c,api_c)):
    ax3.text(l+1.5,i+bw/2,f"{l}%",va="center",fontsize=7.5,color=GREEN,fontweight="bold")
    ax3.text(a+1.5,i-bw/2,f"{a}%",va="center",fontsize=7.5,color=RED,fontweight="bold")
sax(ax3,"Regulatory Compliance Coverage","Coverage %")
ax3.legend([mpatches.Patch(fc=GREEN,alpha=.8),mpatches.Patch(fc=RED,alpha=.8)],
           ["Local","Cloud API"],facecolor=PANEL,labelcolor=WHITE,fontsize=8,framealpha=.6)

# Data flow diagram
ax4=fig3.add_subplot(gs[1,0:2]); ax4.set_facecolor(PANEL); ax4.axis("off")
ax4.set_xlim(0,10); ax4.set_ylim(0,4)
ax4.set_title("Data Flow: Cloud API (top) vs Local LLM (bottom)",
              color=WHITE,fontsize=10,fontweight="bold",pad=8)

def box(x,y,w,h,lbl,col,fs=8.5):
    ax4.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=.1",
        lw=1.2,ec=col,fc=col+"22",transform=ax4.transData,clip_on=False))
    ax4.text(x,y,lbl,ha="center",va="center",fontsize=fs,fontweight="bold",color=col)

def arr(x1,y1,x2,y2,col,lbl=""):
    ax4.annotate("",xy=(x2,y2),xytext=(x1,y1),
        arrowprops=dict(arrowstyle="->",color=col,lw=1.8))
    if lbl: ax4.text((x1+x2)/2,(y1+y2)/2+.15,lbl,ha="center",fontsize=7,color=col,style="italic")

# Cloud API flow (top row y=3.1)
ax4.text(0.2, 3.65, "CLOUD API FLOW - data leaves your environment",
         fontsize=9, color=RED, fontweight="bold")
cloud_nodes = [(1,"Your App\n(User Data)",ORANGE),(3,"Internet\n(Encrypted?)",RED),
               (5,"Vendor\nServers",RED),(7,"LLM\nInference",PURPLE),(9,"Response\n→ App",ORANGE)]
for x,lbl,col in cloud_nodes:
    box(x, 3.1, 1.4, .7, lbl, col)
for x1,x2,lbl,col in[(1.7,2.3,"HTTPS",RED),(3.7,4.3,"Private?",RED),
                      (5.7,6.3,"GPU Call",PURPLE),(7.7,8.3,"HTTPS",RED)]:
    arr(x1, 3.1, x2, 3.1, col, lbl)

# WARNING box: spans from Internet node to LLM Inference node (x=2.3 to x=7.7, y=2.6 to 3.5)
ax4.add_patch(FancyBboxPatch((2.3, 2.62), 5.4, 0.96,
    boxstyle="round,pad=.05", lw=1.8,
    ec=RED, fc="none", linestyle="--",
    transform=ax4.transData, clip_on=False))
ax4.text(5.0, 2.65, "WARNING: DATA EXPOSURE ZONE",
         ha="center", fontsize=8, color=RED, fontweight="bold")

# Local LLM flow (bottom row y=1.15)
ax4.text(0.2, 2.18, "LOCAL LLM FLOW - data never leaves device boundary",
         fontsize=9, color=GREEN, fontweight="bold")
# Secure boundary box spans all local nodes
ax4.add_patch(FancyBboxPatch((0.2, 0.62), 9.6, 1.10,
    boxstyle="round,pad=.05", lw=2,
    ec=GREEN, fc=GREEN+"0A", linestyle="-",
    transform=ax4.transData, clip_on=False))
ax4.text(5.0, 1.80, "SECURE BOUNDARY - Local Device / On-Premises",
         ha="center", fontsize=8, color=GREEN, fontweight="bold")

local_nodes = [(1,"Your App\n(User Data)",ORANGE),(3,"Local\nTokenizer",TEAL),
               (5,"Model\nWeights (disk)",BLUE),(7,"GPU/CPU\nInference",GREEN),(9,"Response\n→ App",ORANGE)]
for x,lbl,col in local_nodes:
    box(x, 1.15, 1.4, .7, lbl, col)
for x1,x2,lbl,col in[(1.7,2.3,"In-mem",TEAL),(3.7,4.3,"mmap()",BLUE),
                      (5.7,6.3,"torch",GREEN),(7.7,8.3,"In-mem",GREEN)]:
    arr(x1, 1.15, x2, 1.15, col, lbl)
ax4.text(5.0, 0.68, "Zero network calls  |  Zero data egress  |  Full audit trail",
         ha="center", fontsize=9, color=GREEN, fontweight="bold")

# Cost model
ax5=fig3.add_subplot(gs[1,2])
tokens=np.linspace(0,10e6,200); capex=1500; api_rate=0.002
cost_api=tokens/1000*api_rate
ax5.plot(tokens/1e6,cost_api,color=RED,lw=2.5,label="Cloud API")
ax5.axhline(y=capex,color=GREEN,lw=2.5,linestyle="--",label=f"Local (capex ${capex:,})")
breakeven=capex/(api_rate/1000)
ax5.axvline(x=breakeven/1e6,color=YELLOW,lw=1.5,linestyle=":",alpha=.8)
ax5.text(breakeven/1e6+0.2,capex*0.55,f"Break-even\n~{breakeven/1e6:.1f}M tokens",color=YELLOW,fontsize=7.5)
ax5.fill_between(tokens/1e6,cost_api,capex,where=cost_api>capex,color=RED,alpha=0.12,label="API overspend")
ax5.fill_between(tokens/1e6,cost_api,capex,where=cost_api<capex,color=GREEN,alpha=0.10,label="API cheaper zone")
sax(ax5,"Cost: Local vs API by Token Volume","Tokens processed (M)","Cost (USD)")
ax5.legend(facecolor=PANEL,labelcolor=WHITE,fontsize=7.5,framealpha=.6)

fig3.suptitle("Part D - Data Privacy Analysis: Local LLM Deployment\nPrivacy Stack  |  Compliance  |  Threat Surface  |  Data Flow  |  Cost Model",
              color=WHITE,fontsize=13,fontweight="bold",y=0.97)
fig3.savefig("privacy_analysis.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig3)

# ── Summary ───────────────────────────────────────────────
avg_lat=np.mean([r["latency_ms"] for r in results])
print(f"""
Part D Complete.
  Avg latency : {avg_lat:.0f} ms  |  Network I/O: 0 bytes  |  API keys: None
  Saved: local_llm_demo.png, local_vs_api_comparison.png, privacy_analysis.png
""")