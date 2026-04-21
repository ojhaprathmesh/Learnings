"""
05_compare_results.py
=====================
Generate a comprehensive side-by-side comparison of baseline vs YOLO-TRP.

Produces
--------
results/comparison/
  comparison_table.png     — publication-ready metrics table
  metric_bars.png          — grouped bar chart of all key metrics
  training_curves.png      — loss & mAP curves overlaid (both models)

Usage
-----
    python 05_compare_results.py

(Run AFTER 04_evaluate.py has written the *_metrics.json files.)
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors

ROOT    = Path(__file__).parent
EVAL_DIR = ROOT / "results" / "evaluation"
OUT_DIR  = ROOT / "results" / "comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RUN_DIR  = ROOT / "runs" / "detect"
CLASS_NAMES = ["Abiotic", "Insect", "Disease"]

MODEL_CFG = {
    "baseline": dict(label="YOLOv8n\n(Baseline)",  color="#4e79a7"),
    "yolo_trp": dict(label="YOLO-TRP\n(Ours)",      color="#e15759"),
}


# -----------------------------------------------------------------------
# Data loading helpers
# -----------------------------------------------------------------------

def load_metrics(model_name: str) -> dict:
    path = EVAL_DIR / f"{model_name}_metrics.json"
    if not path.exists():
        print(f"  ⚠  {path} not found — using placeholder zeros.")
        return {}
    with open(path) as f:
        return json.load(f)


def load_training_csv(model_name: str) -> pd.DataFrame | None:
    csv = RUN_DIR / model_name / "results.csv"
    if not csv.exists():
        return None
    df = pd.read_csv(csv)
    df.columns = [c.strip() for c in df.columns]
    return df


# -----------------------------------------------------------------------
# Plot 1: Grouped bar chart — key metrics
# -----------------------------------------------------------------------

def plot_metric_bars(all_metrics: dict):
    metrics_to_plot = [
        ("mAP50",     "mAP@50"),
        ("mAP50_95",  "mAP@50:95"),
        ("precision", "Precision (mean)"),
        ("recall",    "Recall (mean)"),
        ("mAR",       "mAR"),
        ("mean_iou",  "Mean IoU"),
    ]

    labels  = [m[1] for m in metrics_to_plot]
    models  = list(all_metrics.keys())
    x       = np.arange(len(labels))
    width   = 0.35

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("#f8f8f8")
    ax.set_facecolor("#f8f8f8")
    ax.set_title("Model Comparison — Key Detection Metrics (Test Set)",
                 fontsize=14, fontweight="bold", pad=12)

    for i, mname in enumerate(models):
        cfg    = MODEL_CFG[mname]
        mdata  = all_metrics[mname]
        values = [mdata.get(key, 0.0) or 0.0 for key, _ in metrics_to_plot]
        bars = ax.bar(x + i * width, values, width,
                      label=cfg["label"].replace("\n", " "),
                      color=cfg["color"], alpha=0.88, zorder=3)
        ax.bar_label(bars, fmt="%.3f", padding=3, fontsize=8)

    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Score", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.4, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    out = OUT_DIR / "metric_bars.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {out}")


# -----------------------------------------------------------------------
# Plot 2: Per-class metrics heatmap-style table
# -----------------------------------------------------------------------

def plot_comparison_table(all_metrics: dict):
    rows = []
    models = list(all_metrics.keys())

    for mname in models:
        mdata  = all_metrics[mname]
        cfg    = MODEL_CFG[mname]
        label  = cfg["label"].replace("\n", " ")

        if not mdata:
            continue

        row = {
            "Model":     label,
            "mAP@50":    mdata.get("mAP50", 0),
            "mAP@50:95": mdata.get("mAP50_95", 0),
            "Precision": mdata.get("precision", 0),
            "Recall":    mdata.get("recall", 0),
            "mAR":       mdata.get("mAR", 0),
            "Mean IoU":  mdata.get("mean_iou", 0),
        }

        # Per-class F1
        f1s = mdata.get("per_class_f1", [0, 0, 0])
        for i, cls in enumerate(CLASS_NAMES):
            row[f"F1 {cls}"] = f1s[i] if i < len(f1s) else 0

        rows.append(row)

    if not rows:
        print("  ⚠  No metrics data found to build comparison table.")
        return

    df = pd.DataFrame(rows).set_index("Model")

    fig, ax = plt.subplots(figsize=(16, max(3, len(rows) * 1.5 + 2)))
    ax.axis("off")
    ax.set_title("Detailed Metrics Comparison — CADI-AI Test Set",
                 fontsize=14, fontweight="bold", pad=16)

    col_labels = df.columns.tolist()
    cell_text  = [[f"{v:.4f}" if isinstance(v, float) else str(v) for v in r]
                  for r in df.values]

    tbl = ax.table(
        cellText   = cell_text,
        colLabels  = col_labels,
        rowLabels  = df.index.tolist(),
        cellLoc    = "center",
        rowLoc     = "center",
        loc        = "center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1.4, 1.8)

    # Color header row
    for j in range(len(col_labels)):
        tbl[(0, j)].set_facecolor("#2d6a9f")
        tbl[(0, j)].set_text_props(color="white", fontweight="bold")

    # Color row labels
    for i in range(len(rows)):
        mname  = models[i] if i < len(models) else "unknown"
        color  = MODEL_CFG.get(mname, {}).get("color", "#cccccc")
        tbl[(i + 1, -1)].set_facecolor(color)
        tbl[(i + 1, -1)].set_text_props(color="white", fontweight="bold")

    plt.tight_layout(pad=1.5)
    out = OUT_DIR / "comparison_table.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {out}")


# -----------------------------------------------------------------------
# Plot 3: Training curves — loss + mAP overlay
# -----------------------------------------------------------------------

def plot_training_curves():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Training Curves — Baseline vs YOLO-TRP", fontsize=13, fontweight="bold")

    for ax, (ylabel, csv_col) in zip(
        axes,
        [
            ("Box Loss (val)", "val/box_loss"),
            ("mAP@50 (val)",   "metrics/mAP50(B)"),
        ]
    ):
        for mname, cfg in MODEL_CFG.items():
            df = load_training_csv(mname)
            if df is None or csv_col not in df.columns:
                continue
            ax.plot(df.index + 1, df[csv_col],
                    label=cfg["label"].replace("\n", " "),
                    color=cfg["color"], linewidth=2)

        ax.set_xlabel("Epoch")
        ax.set_ylabel(ylabel)
        ax.set_title(ylabel)
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    out = OUT_DIR / "training_curves.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {out}")


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def main():
    print("\n" + "=" * 60)
    print("  YOLO-TRP Assignment — Comparison Report")
    print("=" * 60)

    all_metrics = {mname: load_metrics(mname) for mname in MODEL_CFG}

    print("\n[1/3] Generating metric bar chart …")
    plot_metric_bars(all_metrics)

    print("[2/3] Generating comparison table …")
    plot_comparison_table(all_metrics)

    print("[3/3] Generating training curves …")
    plot_training_curves()

    print(f"\n✅  Comparison report saved to: {OUT_DIR}")
    print("    Files:")
    for f in sorted(OUT_DIR.iterdir()):
        print(f"      {f.name}")


if __name__ == "__main__":
    main()
