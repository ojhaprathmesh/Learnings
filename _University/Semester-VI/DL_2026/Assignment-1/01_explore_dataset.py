"""
01_explore_dataset.py
=====================
CADI-AI Dataset Exploration and Preparation
============================================
Generates:
- Class distribution bar chart + pie chart
- Sample annotated images (bounding boxes overlaid)
- BBox size & aspect-ratio statistics per class
- Split summary table printed to console
- All plots saved to  results/exploration/
"""

import os
import sys
import json
import random
from pathlib import Path
from collections import defaultdict

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import yaml

# -----------------------------------------------------------------------
ROOT = Path(__file__).parent
DATA_YAML = ROOT / "dataset.yaml"


def _resolve_splits_from_yaml(dataset_yaml: Path) -> dict[str, Path]:
    cfg = yaml.safe_load(dataset_yaml.read_text(encoding="utf-8"))
    base = Path(cfg.get("path", ROOT))
    splits: dict[str, Path] = {}
    for split in ("train", "val", "test"):
        split_images = cfg.get(split)
        if split_images:
            img_dir = base / str(split_images)
            splits[split] = img_dir.parent  # contains images/ and labels/
    return splits


SPLITS = _resolve_splits_from_yaml(DATA_YAML) if DATA_YAML.exists() else {}
CLASS_NAMES = {0: "abiotic", 1: "insect", 2: "disease"}
COLORS      = {0: "#e05c5c", 1: "#5c8fe0", 2: "#5cbf7e"}

OUT_DIR = ROOT / "results" / "exploration"
OUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)
# -----------------------------------------------------------------------


def load_split(split_dir: Path):
    """Return lists of (image_path, label_path) pairs for a split."""
    img_dir = split_dir / "images"
    lbl_dir = split_dir / "labels"
    pairs = []
    for img_path in sorted(img_dir.iterdir()):
        lbl_path = lbl_dir / img_path.with_suffix(".txt").name
        if lbl_path.exists():
            pairs.append((img_path, lbl_path))
    return pairs


def parse_label_file(lbl_path: Path):
    """Return list of (class_id, cx, cy, w, h) tuples."""
    rows = []
    with open(lbl_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            rows.append((int(parts[0]), *map(float, parts[1:])))
    return rows


def gather_stats():
    """Collect annotation counts and bbox statistics across all splits."""
    stats = {}
    for split_name, split_dir in SPLITS.items():
        pairs = load_split(split_dir)
        class_counts = defaultdict(int)
        bbox_areas   = defaultdict(list)
        bbox_aspects = defaultdict(list)

        for _, lbl_path in pairs:
            for cls, cx, cy, w, h in parse_label_file(lbl_path):
                class_counts[cls] += 1
                bbox_areas[cls].append(w * h)
                bbox_aspects[cls].append(w / (h + 1e-6))

        stats[split_name] = {
            "n_images":     len(pairs),
            "class_counts": dict(class_counts),
            "bbox_areas":   bbox_areas,
            "bbox_aspects": bbox_aspects,
        }
    return stats


# -----------------------------------------------------------------------
# Plot helpers
# -----------------------------------------------------------------------

def plot_class_distribution(stats):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("CADI-AI — Class Distribution Across Splits", fontsize=14, fontweight="bold")

    split_names = list(stats.keys())
    x = np.arange(len(CLASS_NAMES))
    width = 0.25

    ax = axes[0]
    for i, split in enumerate(split_names):
        counts = [stats[split]["class_counts"].get(c, 0) for c in CLASS_NAMES]
        ax.bar(x + i * width, counts, width, label=split.capitalize(),
               color=["#4e79a7", "#f28e2b", "#59a14f"][i], alpha=0.85)
    ax.set_xticks(x + width)
    ax.set_xticklabels([CLASS_NAMES[c].capitalize() for c in CLASS_NAMES])
    ax.set_ylabel("Annotation Count")
    ax.set_title("Per-Class Annotation Counts by Split")
    ax.legend()
    ax.grid(axis="y", alpha=0.4)

    # Pie chart (train only)
    ax2 = axes[1]
    train_counts = [stats["train"]["class_counts"].get(c, 0) for c in CLASS_NAMES]
    labels = [f"{CLASS_NAMES[c].capitalize()}\n({train_counts[i]})"
              for i, c in enumerate(CLASS_NAMES)]
    wedge_colors = [COLORS[c] for c in CLASS_NAMES]
    ax2.pie(train_counts, labels=labels, colors=wedge_colors, autopct="%1.1f%%",
            startangle=140, pctdistance=0.8)
    ax2.set_title("Train Split — Class Proportions")

    plt.tight_layout()
    out = OUT_DIR / "class_distribution.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {out}")


def plot_bbox_statistics(stats):
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle("CADI-AI — BBox Size & Aspect-Ratio (Train Split)", fontsize=13, fontweight="bold")

    for col, cls in enumerate(CLASS_NAMES):
        areas   = stats["train"]["bbox_areas"].get(cls, [])
        aspects = stats["train"]["bbox_aspects"].get(cls, [])

        # Area histogram
        ax = axes[0][col]
        ax.hist(areas, bins=50, color=COLORS[cls], alpha=0.8, edgecolor="white")
        ax.set_title(f"{CLASS_NAMES[cls].capitalize()} — BBox Area (w×h, normalised)")
        ax.set_xlabel("Normalised Area")
        ax.set_ylabel("Count")
        ax.axvline(np.median(areas), color="black", linestyle="--", label=f"median={np.median(areas):.4f}")
        ax.legend(fontsize=8)

        # Aspect-ratio histogram
        ax = axes[1][col]
        ax.hist(aspects, bins=50, color=COLORS[cls], alpha=0.8, edgecolor="white")
        ax.set_title(f"{CLASS_NAMES[cls].capitalize()} — Aspect Ratio (w/h)")
        ax.set_xlabel("Aspect Ratio")
        ax.set_ylabel("Count")
        ax.axvline(np.median(aspects), color="black", linestyle="--", label=f"median={np.median(aspects):.2f}")
        ax.legend(fontsize=8)

    plt.tight_layout()
    out = OUT_DIR / "bbox_statistics.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {out}")


def draw_boxes_on_image(img_bgr, annotations):
    """Draw YOLO-format bounding boxes on a BGR image copy."""
    img = img_bgr.copy()
    h, w = img.shape[:2]

    color_map_bgr = {
        0: (92,  92, 224),   # red  → abiotic
        1: (224, 143,  92),  # blue → insect
        2: (126, 191,  92),  # green→ disease
    }

    for cls, cx, cy, bw, bh in annotations:
        x1 = int((cx - bw / 2) * w)
        y1 = int((cy - bh / 2) * h)
        x2 = int((cx + bw / 2) * w)
        y2 = int((cy + bh / 2) * h)
        c  = color_map_bgr.get(cls, (255, 255, 255))
        cv2.rectangle(img, (x1, y1), (x2, y2), c, 2)
        label = CLASS_NAMES.get(cls, str(cls))
        cv2.putText(img, label, (x1, max(0, y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, c, 1, cv2.LINE_AA)
    return img


def plot_sample_images(stats, n_per_class: int = 3):
    """Show annotated sample images for each class from the train split."""
    train_pairs = load_split(SPLITS["train"])

    # Group images by which classes appear in them
    class_to_pairs = defaultdict(list)
    for pair in train_pairs:
        _, lbl = pair
        anns = parse_label_file(lbl)
        classes_present = {a[0] for a in anns}
        for c in classes_present:
            class_to_pairs[c].append(pair)

    fig, axes = plt.subplots(3, n_per_class, figsize=(5 * n_per_class, 12))
    fig.suptitle("CADI-AI — Sample Annotated Images per Class", fontsize=14, fontweight="bold")

    for row, cls in enumerate(CLASS_NAMES):
        samples = random.sample(class_to_pairs[cls], min(n_per_class, len(class_to_pairs[cls])))
        for col, (img_path, lbl_path) in enumerate(samples):
            img_bgr = cv2.imread(str(img_path))
            if img_bgr is None:
                continue
            anns = parse_label_file(lbl_path)
            annotated = draw_boxes_on_image(img_bgr, anns)
            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

            ax = axes[row][col]
            ax.imshow(annotated_rgb)
            ax.axis("off")
            if col == 0:
                ax.set_ylabel(CLASS_NAMES[cls].capitalize(), fontsize=12, fontweight="bold")

    plt.tight_layout()
    out = OUT_DIR / "sample_images.png"
    plt.savefig(out, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {out}")


def print_summary(stats):
    print("\n" + "=" * 60)
    print("  CADI-AI Dataset Summary")
    print("=" * 60)
    header = f"{'Split':<8}{'Images':>8}{'Abiotic':>10}{'Insect':>10}{'Disease':>10}{'Total':>10}"
    print(header)
    print("-" * 60)
    for split, s in stats.items():
        counts = [s["class_counts"].get(c, 0) for c in CLASS_NAMES]
        total  = sum(counts)
        print(f"{split.capitalize():<8}{s['n_images']:>8}{counts[0]:>10}{counts[1]:>10}{counts[2]:>10}{total:>10}")
    print("=" * 60)

    # BBox statistics
    print("\n  Train BBox Statistics (normalised)")
    print(f"  {'Class':<10}  {'Median Area':>13}  {'Median Aspect':>14}")
    print("  " + "-" * 40)
    for cls in CLASS_NAMES:
        areas   = stats["train"]["bbox_areas"].get(cls, [1])
        aspects = stats["train"]["bbox_aspects"].get(cls, [1])
        print(f"  {CLASS_NAMES[cls]:<10}  {np.median(areas):>13.5f}  {np.median(aspects):>14.3f}")

    # Save JSON for report
    out_json = OUT_DIR / "dataset_stats.json"
    json_safe = {}
    for split, s in stats.items():
        json_safe[split] = {
            "n_images":     s["n_images"],
            "class_counts": s["class_counts"],
        }
    with open(out_json, "w") as f:
        json.dump(json_safe, f, indent=2)
    print(f"\n  ✓ Saved {out_json}")


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

if __name__ == "__main__":
    print("\n[1/4] Gathering annotation statistics …")
    stats = gather_stats()

    print("[2/4] Plotting class distribution …")
    plot_class_distribution(stats)

    print("[3/4] Plotting bbox statistics …")
    plot_bbox_statistics(stats)

    print("[4/4] Plotting sample images …")
    plot_sample_images(stats)

    print_summary(stats)
    print("\n✅  Exploration complete.  Figures saved to:", OUT_DIR)
