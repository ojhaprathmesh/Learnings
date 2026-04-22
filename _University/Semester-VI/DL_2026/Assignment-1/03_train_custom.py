"""
03_train_custom.py
==================
Train the YOLO-TRP model on the CADI-AI dataset.

Modifications over YOLOv8n baseline
-------------------------------------
1. CBAM attention after every C2f backbone stage
   → Channel + spatial attention for discriminative feature focus.
2. TransformerNeck after SPPF
   → Long-range context at stride-32 feature maps (20×20 tokens).
3. Focal Loss (γ=2) with class-frequency inverse weighting
   → Addresses severe class imbalance (abiotic 7 %, insect 62 %, disease 31 %).

Results are saved to  runs/detect/yolo_trp/

Usage
-----
    python 03_train_custom.py
"""

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# -----------------------------------------------------------------------
# RTX 40xx Laptop GPU fix: torch.cuda.synchronize() causes CUDA illegal
# instruction/memory access in Ultralytics' Profile timing class on
# PyTorch 2.5.x + Windows. Patch it to skip sync — only affects profiling.
# -----------------------------------------------------------------------
import ultralytics.utils.ops as _ul_ops
_ul_ops.Profile.time = lambda self: time.perf_counter()

from custom_model.yolo_trp_trainer import YOLOTRPTrainer
import torch

RUNS_DIR = Path(os.getenv("YOLO_RUNS_DIR", str(ROOT / "runs" / "detect")))
RUN_DIR = RUNS_DIR / "yolo_trp"
LAST_CKPT = RUN_DIR / "weights" / "last.pt"

# -----------------------------------------------------------------------
# Hyperparameters   (same as baseline for fair comparison,
#                    except pretrained=False because the custom YAML
#                    has a different structure from COCO-pretrained weights)
# -----------------------------------------------------------------------
OVERRIDES = dict(
    model  = str(ROOT / "custom_model" / "yolo_trp.yaml"),
    data   = str(ROOT / "dataset.yaml"),
    epochs = 32,
    imgsz  = 640,
    batch  = 8,                        # RTX 40xx laptop: batch=8 for stability
    device = 0,
    workers= 0,                        # 0 workers avoids multiprocess CUDA issues on Windows
    amp    = False,                    # Disable AMP — fixes CUDA illegal memory access on RTX 40xx Windows
    deterministic = False,             # Disable deterministic mode — avoids adaptive_max_pool CUDA crash
    optimizer   = "AdamW",
    lr0         = 5e-4,                # Lower LR for scratch-init stability (TransformerNeck)
    lrf         = 0.01,
    momentum    = 0.937,
    weight_decay= 5e-4,
    warmup_epochs = 5,                 # Longer warmup for scratch training
    # Data augmentation — identical to baseline for fair comparison
    augment   = True,
    mosaic    = 1.0,
    mixup     = 0.15,          # slight mixup (extra aug for rare classes)
    hsv_h     = 0.015,
    hsv_s     = 0.7,
    hsv_v     = 0.4,
    flipud    = 0.1,
    fliplr    = 0.5,
    # Logging / saving
    project    = str(RUNS_DIR),
    name       = "yolo_trp",
    save        = True,
    save_period = 1,                    # Save checkpoint every epoch for safer resume
    exist_ok    = True,
    val         = True,
    plots       = True,
    verbose     = True,
    pretrained  = False,       # fresh weights — CBAM+Transformer not in COCO
)


def _resolve_runtime_overrides(overrides: dict) -> dict:
    runtime_overrides = dict(overrides)
    if torch.cuda.is_available():
        runtime_overrides["device"] = 0
    else:
        runtime_overrides["device"] = "cpu"
        runtime_overrides["batch"] = min(2, int(overrides.get("batch", 8)))
        runtime_overrides["workers"] = 0
        runtime_overrides["amp"] = False
        print("\n  [WARN] CUDA is not available in this Python environment.")
        print("         Falling back to CPU mode (very slow).")
    return runtime_overrides


def _train_with_retry(overrides: dict) -> None:
    trainer = YOLOTRPTrainer(overrides=overrides)
    try:
        trainer.train()
    except RuntimeError as exc:
        msg = str(exc)
        if "CUDA error: an illegal instruction was encountered" not in msg:
            raise
        print("\n  [WARN] CUDA illegal instruction encountered.")
        print("         Retrying with safer settings (smaller batch + blocking launches).")
        os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        retry_overrides = dict(overrides)
        retry_overrides["batch"] = max(2, int(overrides.get("batch", 8)) // 2)
        retry_overrides["val"] = False  # avoid validator CUDA path in unstable sessions
        print(f"         Retry batch size: {retry_overrides['batch']}")
        YOLOTRPTrainer(overrides=retry_overrides).train()


def main():
    print("=" * 60)
    print("  YOLO-TRP — Custom Architecture Training")
    print("=" * 60)
    print("\n  Modifications:")
    print("    • CBAM attention after each C2f backbone stage (layers 3,6,9)")
    print("    • TransformerNeck after SPPF        (layer 13)")
    print("    • Focal Loss (γ=2) + class weights  [8.85, 1.00, 2.02]")
    print(f"\n  Model YAML  : {OVERRIDES['model']}")
    print(f"  Data        : {OVERRIDES['data']}")
    print(f"  Epochs      : {OVERRIDES['epochs']}")
    runtime_overrides = _resolve_runtime_overrides(OVERRIDES)

    print(f"  Batch size  : {runtime_overrides['batch']}")
    print(f"  Image size  : {OVERRIDES['imgsz']}")
    print(f"  Device      : {runtime_overrides['device']}")
    print(f"  Saving to   : {OVERRIDES['project']}/{OVERRIDES['name']}")

    run_overrides = dict(runtime_overrides)
    if LAST_CKPT.exists():
        run_overrides["resume"] = str(LAST_CKPT)
        print(f"  Resume      : Yes ({LAST_CKPT})\n")
    else:
        print("  Resume      : No (starting fresh)\n")

    _train_with_retry(run_overrides)

    # Print final metrics from saved results CSV
    results_csv = ROOT / "runs" / "detect" / "yolo_trp" / "results.csv"
    if results_csv.exists():
        import pandas as pd
        df = pd.read_csv(results_csv)
        df.columns = [c.strip() for c in df.columns]
        last = df.iloc[-1]
        map50    = last.get("metrics/mAP50(B)",    "N/A")
        map5095  = last.get("metrics/mAP50-95(B)", "N/A")
        print("\n" + "=" * 60)
        print("  YOLO-TRP training complete.")
        print(f"  Best weights: {OVERRIDES['project']}/{OVERRIDES['name']}/weights/best.pt")
        try:
            print(f"  mAP@50     : {float(map50):.4f}")
            print(f"  mAP@50:95  : {float(map5095):.4f}")
        except (TypeError, ValueError):
            pass
        print("=" * 60)


if __name__ == "__main__":
    main()
