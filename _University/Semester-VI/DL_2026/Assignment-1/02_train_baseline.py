"""
02_train_baseline.py
====================
Train a baseline YOLOv8n model on the CADI-AI dataset.
Results are saved to  runs/detect/baseline/

Usage
-----
    python 02_train_baseline.py
"""

import os
import sys
import time
from pathlib import Path

# -----------------------------------------------------------------------
# RTX 40xx Laptop GPU fix: torch.cuda.synchronize() causes CUDA illegal
# instruction/memory access in Ultralytics' Profile timing class on
# PyTorch 2.5.x + Windows. Patch it to skip sync — only affects profiling.
# -----------------------------------------------------------------------
import ultralytics.utils.ops as _ul_ops
_ul_ops.Profile.time = lambda self: time.perf_counter()

from ultralytics import YOLO
import torch

ROOT = Path(__file__).parent
RUN_DIR = ROOT / "runs" / "detect" / "baseline"
LAST_CKPT = RUN_DIR / "weights" / "last.pt"

# -----------------------------------------------------------------------
# Hyperparameters
# -----------------------------------------------------------------------
CFG = dict(
    model  = "yolov8n.yaml",          # nano architecture (pretrained weights)
    data   = str(ROOT / "dataset.yaml"),
    epochs = 32,
    imgsz  = 640,
    batch  = 8,                        # RTX 40xx laptop: batch=8 for stability
    device = 0,                        # GPU 0; set to "cpu" if no GPU
    workers= 0,                        # 0 workers avoids multiprocess CUDA issues on Windows
    amp    = False,                    # Disable AMP — fixes CUDA illegal instruction on RTX 40xx Windows
    deterministic = False,             # Disable deterministic mode — avoids adaptive_max_pool CUDA crash
    optimizer  = "AdamW",
    lr0        = 1e-3,
    lrf        = 0.01,
    momentum   = 0.937,
    weight_decay = 5e-4,
    warmup_epochs = 3,
    # Data augmentation
    augment    = True,
    mosaic     = 1.0,
    mixup      = 0.0,
    hsv_h      = 0.015,
    hsv_s      = 0.7,
    hsv_v      = 0.4,
    flipud     = 0.1,
    fliplr     = 0.5,
    # Logging / saving
    project    = str(ROOT / "runs" / "detect"),
    name       = "baseline",
    save        = True,
    save_period = 1,                    # Save checkpoint every epoch for safer resume
    exist_ok    = True,
    val         = True,
    plots       = True,
    verbose     = True,
    # Pretrained weights — download YOLOv8n COCO weights for transfer learning
    pretrained = True,
)


def _resolve_runtime_cfg(cfg: dict) -> dict:
    runtime_cfg = dict(cfg)
    if torch.cuda.is_available():
        runtime_cfg["device"] = 0
    else:
        # Keep pipeline runnable even when a CPU-only torch wheel is installed.
        runtime_cfg["device"] = "cpu"
        runtime_cfg["batch"] = min(2, int(cfg.get("batch", 8)))
        runtime_cfg["workers"] = 0
        runtime_cfg["amp"] = False
        print("\n  [WARN] CUDA is not available in this Python environment.")
        print("         Falling back to CPU mode (very slow).")
    return runtime_cfg


def _print_metric(label: str, value) -> None:
    try:
        print(f"  {label:<11}: {float(value):.4f}")
    except (TypeError, ValueError):
        print(f"  {label:<11}: N/A")


def _train_with_retry(model: YOLO, cfg: dict):
    try:
        return model.train(**cfg)
    except RuntimeError as exc:
        msg = str(exc)
        if "CUDA error: an illegal instruction was encountered" not in msg:
            raise
        print("\n  [WARN] CUDA illegal instruction encountered.")
        print("         Retrying with safer settings (smaller batch + blocking launches).")
        os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        retry_cfg = dict(cfg)
        retry_cfg["batch"] = max(2, int(cfg.get("batch", 8)) // 2)
        retry_cfg["val"] = False  # avoid validator CUDA path in unstable sessions
        print(f"         Retry batch size: {retry_cfg['batch']}")
        return model.train(**retry_cfg)


def main():
    print("=" * 60)
    print("  YOLO-TRP Assignment — Baseline YOLOv8n Training")
    print("=" * 60)

    print(f"\n  Model     : YOLOv8n (pretrained COCO)")
    print(f"  Data      : {CFG['data']}")
    print(f"  Epochs    : {CFG['epochs']}")
    runtime_cfg = _resolve_runtime_cfg(CFG)

    print(f"  Batch size: {runtime_cfg['batch']}")
    print(f"  Image size: {CFG['imgsz']}")
    print(f"  Device    : {runtime_cfg['device']}")
    print(f"  Saving to : {CFG['project']}/{CFG['name']}")

    if LAST_CKPT.exists():
        print(f"  Resume    : Yes ({LAST_CKPT})\n")
        model = YOLO(str(LAST_CKPT))
        results = model.train(resume=True)
    else:
        print("  Resume    : No (starting fresh)\n")
        # Load YOLOv8n with COCO pretrained weights for transfer learning
        model = YOLO("yolov8n.pt")
        results = _train_with_retry(model, runtime_cfg)

    print("\n" + "=" * 60)
    print("  Baseline training complete.")
    print(f"  Best weights: {CFG['project']}/{CFG['name']}/weights/best.pt")
    _print_metric("mAP@50", results.results_dict.get("metrics/mAP50(B)"))
    _print_metric("mAP@50:95", results.results_dict.get("metrics/mAP50-95(B)"))
    print("=" * 60)


if __name__ == "__main__":
    main()
