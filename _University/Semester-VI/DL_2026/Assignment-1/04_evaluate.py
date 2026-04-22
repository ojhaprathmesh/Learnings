"""
04_evaluate.py
==============
Comprehensive evaluation of both models on the CADI-AI test set.

Metrics generated
-----------------
- mAP@0.50, mAP@0.50:0.95 (area under PR curve)
- Mean Average Recall (mAR)
- Per-class Precision, Recall, F1-score
- Precision-Recall curves (per class + combined)
- IoU distribution histogram (how well boxes are localised)

Output
------
results/
  evaluation/
    baseline_metrics.json
    yolo_trp_metrics.json
    pr_curves.png
    iou_distribution.png
    per_class_f1.png

Usage
-----
    python 04_evaluate.py
"""

import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from ultralytics import YOLO
import yaml

ROOT = Path(__file__).parent
RUNS_DIR = Path(os.getenv("YOLO_RUNS_DIR", str(ROOT / "runs" / "detect")))
RESULTS_DIR = Path(os.getenv("YOLO_RESULTS_DIR", str(ROOT / "results")))

BASELINE_WEIGHTS = RUNS_DIR / "baseline" / "weights" / "best.pt"
CUSTOM_WEIGHTS   = RUNS_DIR / "yolo_trp" / "weights" / "best.pt"
DATA_YAML        = str(ROOT / "dataset.yaml")

OUT_DIR = RESULTS_DIR / "evaluation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CLASS_NAMES = ["abiotic", "insect", "disease"]
CLASS_COLORS = ["#e05c5c", "#5c8fe0", "#5cbf7e"]

MODEL_STYLES = {
    "baseline":  dict(color="#4e79a7", linestyle="-",  label="YOLOv8n (Baseline)"),
    "yolo_trp":  dict(color="#e15759", linestyle="--", label="YOLO-TRP (Ours)"),
}


# -----------------------------------------------------------------------
# Core evaluation function
# -----------------------------------------------------------------------

def evaluate_model(weights_path: Path, model_name: str) -> dict:
    """Run model.val() on the test split and return a cleaned metrics dict."""
    print(f"\n  Evaluating: {model_name}  ({weights_path})")

    if not weights_path.exists():
        print(f"  ⚠  Weights not found at {weights_path}. Skipping.")
        return {}

    model = YOLO(str(weights_path))
    val_results = model.val(
        data    = DATA_YAML,
        split   = "test",
        imgsz   = 640,
        batch   = 16,
        conf    = 0.001,    # low conf to capture full PR curve
        iou     = 0.60,
        plots   = True,
        save_json = True,
        project = str(OUT_DIR / model_name),
        name    = "eval",
        exist_ok= True,
        verbose = False,
    )

    metrics = {
        "model":       model_name,
        "mAP50":       float(val_results.box.map50),
        "mAP50_95":    float(val_results.box.map),
        "precision":   float(val_results.box.mp),
        "recall":      float(val_results.box.mr),
        "per_class_mAP50": [float(v) for v in val_results.box.maps],
        # val_results.box.p, .r are per-class precision/recall arrays
        "per_class_precision": [float(v) for v in val_results.box.p],
        "per_class_recall":    [float(v) for v in val_results.box.r],
    }

    # F1 per class
    metrics["per_class_f1"] = [
        2 * p * r / (p + r + 1e-9)
        for p, r in zip(metrics["per_class_precision"], metrics["per_class_recall"])
    ]

    # Mean AR = mean recall across classes
    metrics["mAR"] = float(np.mean(metrics["per_class_recall"]))

    # ---- PR curve data (per class) ----------------------------------------
    # Ultralytics stores curve data in val_results.box.{curves}
    # 'curves' exist only in newer versions; guard accordingly
    pr_curves = {}
    try:
        px   = val_results.box.px         # confidence thresholds
        py   = val_results.box.py         # precision (nc, thresholds)
        prec_r = val_results.box.prec_results if hasattr(val_results.box, "prec_results") else None

        # Ultralytics new API (≥8.1): curves stored as {class: (R, P)}
        if hasattr(val_results.box, "curves_results"):
            for i, cr in enumerate(val_results.box.curves_results):
                pr_curves[CLASS_NAMES[i]] = {
                    "recall":    cr[0].tolist() if hasattr(cr[0], "tolist") else list(cr[0]),
                    "precision": cr[1].tolist() if hasattr(cr[1], "tolist") else list(cr[1]),
                }
    except Exception:
        pass  # PR curve arrays not always available; plots saved by Ultralytics separately

    metrics["pr_curves"] = pr_curves

    # Save
    out_path = OUT_DIR / f"{model_name}_metrics.json"
    with open(out_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"  ✓ Saved {out_path}")

    return metrics


# -----------------------------------------------------------------------
# IoU distribution (via custom inference)
# -----------------------------------------------------------------------

def compute_iou_distribution(weights_path: Path, model_name: str, n_images: int = 200):
    """
    Run inference on test images, match predictions to GT by greedy IoU,
    return list of matched IoU values.
    """
    if not weights_path.exists():
        return []

    import cv2
    from pathlib import Path as P

    model = YOLO(str(weights_path))

    # Resolve test directories from dataset.yaml so it works on Drive layouts too.
    cfg = yaml.safe_load((ROOT / "dataset.yaml").read_text(encoding="utf-8"))
    base = Path(cfg.get("path", ROOT))
    test_images = base / str(cfg.get("test", "test/images"))
    test_imgs = list(test_images.iterdir())[:n_images]
    test_lbls = test_images.parent / "labels"

    ious = []
    for img_path in test_imgs:
        lbl_path = test_lbls / img_path.with_suffix(".txt").name
        if not lbl_path.exists():
            continue

        # Ground truth boxes  (xyxy normalised)
        gt = []
        with open(lbl_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                cls, cx, cy, w, h = int(parts[0]), *map(float, parts[1:])
                x1, y1 = cx - w / 2, cy - h / 2
                x2, y2 = cx + w / 2, cy + h / 2
                gt.append([x1, y1, x2, y2])

        if not gt:
            continue

        # Predictions
        res = model.predict(str(img_path), conf=0.25, verbose=False)[0]
        if res.boxes is None or len(res.boxes) == 0:
            continue

        H, W = res.orig_shape
        pred_boxes = res.boxes.xyxyn.cpu().numpy()  # normalised xyxy

        gt_arr   = np.array(gt)
        pred_arr = pred_boxes

        # Compute pairwise IoU
        for pb in pred_arr:
            best_iou = 0.0
            for gb in gt_arr:
                ix1 = max(pb[0], gb[0]);  iy1 = max(pb[1], gb[1])
                ix2 = min(pb[2], gb[2]);  iy2 = min(pb[3], gb[3])
                inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
                ua    = (pb[2]-pb[0])*(pb[3]-pb[1]) + (gb[2]-gb[0])*(gb[3]-gb[1]) - inter
                best_iou = max(best_iou, inter / (ua + 1e-9))
            ious.append(best_iou)

    return ious


# -----------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------

def plot_pr_curves(all_metrics: dict):
    """Plot Precision-Recall curves if curves data is available."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Precision-Recall Curves (Test Set)", fontsize=13, fontweight="bold")

    for col, cls_name in enumerate(CLASS_NAMES):
        ax = axes[col]
        ax.set_title(cls_name.capitalize(), fontsize=11)
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1.05)
        ax.grid(alpha=0.3)

        for mname, mdata in all_metrics.items():
            if not mdata or "pr_curves" not in mdata:
                continue
            style = MODEL_STYLES.get(mname, {})
            pr    = mdata["pr_curves"].get(cls_name)
            if pr:
                ax.plot(pr["recall"], pr["precision"],
                        color=style.get("color", "grey"),
                        linestyle=style.get("linestyle", "-"),
                        label=style.get("label", mname), linewidth=2)
            else:
                # Fall back: plot single point (P, R)
                idx = CLASS_NAMES.index(cls_name)
                p = mdata["per_class_precision"][idx]
                r = mdata["per_class_recall"][idx]
                ax.scatter([r], [p], s=80,
                           color=style.get("color", "grey"),
                           label=style.get("label", mname) + " (point)", zorder=5)

        ax.legend(fontsize=8)

    plt.tight_layout()
    out = OUT_DIR / "pr_curves.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {out}")


def plot_iou_distributions(iou_data: dict):
    """IoU histogram for each model."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_title("IoU Distribution of Matched Predictions (Test Set)", fontsize=12)
    ax.set_xlabel("Best-Match IoU")
    ax.set_ylabel("Count")

    for mname, ious in iou_data.items():
        if not ious:
            continue
        style = MODEL_STYLES.get(mname, {})
        ax.hist(ious, bins=40, alpha=0.55,
                color=style.get("color", "grey"),
                label=style.get("label", mname))
        mean_iou = np.mean(ious)
        ax.axvline(mean_iou, linestyle="--", color=style.get("color", "grey"),
                   label=f"{style.get('label', mname)} mean={mean_iou:.3f}")

    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    out = OUT_DIR / "iou_distribution.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {out}")


def plot_per_class_f1(all_metrics: dict):
    """Side-by-side bar chart of per-class F1."""
    models = [m for m, d in all_metrics.items() if d]
    x = np.arange(len(CLASS_NAMES))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title("Per-Class F1-Score (Test Set)", fontsize=12)
    ax.set_xticks(x + width / 2 * (len(models) - 1))
    ax.set_xticklabels([c.capitalize() for c in CLASS_NAMES])
    ax.set_ylabel("F1-Score")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", alpha=0.3)

    for i, mname in enumerate(models):
        mdata = all_metrics[mname]
        if not mdata:
            continue
        style = MODEL_STYLES.get(mname, {})
        f1s   = mdata.get("per_class_f1", [])
        bars  = ax.bar(x + i * width, f1s, width,
                       label=style.get("label", mname),
                       color=style.get("color", "grey"), alpha=0.85)
        ax.bar_label(bars, fmt="%.3f", padding=2, fontsize=9)

    ax.legend()
    plt.tight_layout()
    out = OUT_DIR / "per_class_f1.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {out}")


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def main():
    print("\n" + "=" * 60)
    print("  YOLO-TRP Assignment — Evaluation")
    print("=" * 60)

    all_metrics: dict = {}

    print("\n[1/4] Evaluating baseline model …")
    all_metrics["baseline"] = evaluate_model(BASELINE_WEIGHTS, "baseline")

    print("\n[2/4] Evaluating YOLO-TRP model …")
    all_metrics["yolo_trp"] = evaluate_model(CUSTOM_WEIGHTS, "yolo_trp")

    print("\n[3/4] Computing IoU distributions …")
    iou_data = {
        "baseline": compute_iou_distribution(BASELINE_WEIGHTS, "baseline"),
        "yolo_trp": compute_iou_distribution(CUSTOM_WEIGHTS,   "yolo_trp"),
    }
    plot_iou_distributions(iou_data)
    # Save means
    for mname, ious in iou_data.items():
        if mname in all_metrics and all_metrics[mname]:
            all_metrics[mname]["mean_iou"] = float(np.mean(ious)) if ious else 0.0

    print("\n[4/4] Generating plots …")
    plot_pr_curves(all_metrics)
    plot_per_class_f1(all_metrics)

    # Re-save JSON with IoU means
    for mname, mdata in all_metrics.items():
        if mdata:
            with open(OUT_DIR / f"{mname}_metrics.json", "w") as f:
                mdata_out = {k: v for k, v in mdata.items() if k != "pr_curves"}
                json.dump(mdata_out, f, indent=2)

    # Print summary table
    print("\n" + "=" * 70)
    print(f"  {'Metric':<20}  {'Baseline (YOLOv8n)':>20}  {'YOLO-TRP (Ours)':>20}")
    print("  " + "-" * 65)
    metric_keys = [
        ("mAP50",     "mAP@50"),
        ("mAP50_95",  "mAP@50:95"),
        ("precision", "Precision"),
        ("recall",    "Recall"),
        ("mAR",       "mAR"),
        ("mean_iou",  "Mean IoU"),
    ]
    for key, label in metric_keys:
        bv = all_metrics.get("baseline", {}).get(key, "—")
        cv = all_metrics.get("yolo_trp", {}).get(key, "—")
        bvs = f"{bv:.4f}" if isinstance(bv, float) else str(bv)
        cvs = f"{cv:.4f}" if isinstance(cv, float) else str(cv)
        print(f"  {label:<20}  {bvs:>20}  {cvs:>20}")
    print("=" * 70)
    print(f"\n✅  Evaluation complete.  Results saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
