"""
utils.py - Shared utilities: logging, seed setting, device detection, checkpoint helpers.
"""

import logging
import os
import random
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import torch


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(
    log_level: int = logging.INFO,
    log_dir: Optional[str] = None,
    log_file: str = "training.log",
) -> logging.Logger:
    """
    Configure root logger with a StreamHandler and optional FileHandler.
    Returns the root logger.
    """
    handlers = [logging.StreamHandler(sys.stdout)]

    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            os.path.join(log_dir, log_file), mode="a", encoding="utf-8"
        )
        handlers.append(file_handler)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )

    # Reduce verbosity of noisy third-party loggers
    for noisy in ("transformers", "datasets", "tokenizers", "huggingface_hub"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    return logging.getLogger()


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------

def set_seed(seed: int = 42) -> None:
    """Set random seeds for Python, NumPy, and PyTorch."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    # Makes CUDA operations deterministic (slower but reproducible)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# ---------------------------------------------------------------------------
# Device / hardware helpers
# ---------------------------------------------------------------------------

def get_device() -> str:
    """Return the best available device string."""
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def log_hardware_info() -> None:
    """Log GPU / CPU info for the experiment record."""
    logger = logging.getLogger(__name__)
    logger.info("PyTorch version : %s", torch.__version__)
    if torch.cuda.is_available():
        logger.info("CUDA available  : True")
        logger.info("CUDA version    : %s", torch.version.cuda)
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            logger.info(
                "  GPU %d: %s | VRAM: %.1f GB",
                i, props.name, props.total_memory / 1e9,
            )
    else:
        logger.info("CUDA available  : False (running on CPU)")


# ---------------------------------------------------------------------------
# Checkpoint helpers
# ---------------------------------------------------------------------------

def get_latest_checkpoint(checkpoint_dir: str) -> Optional[str]:
    """
    Scan a directory for HuggingFace-style checkpoint folders
    (named checkpoint-<step>) and return the path to the latest one.
    """
    checkpoint_dir = Path(checkpoint_dir)
    if not checkpoint_dir.exists():
        return None
    checkpoints = sorted(
        [d for d in checkpoint_dir.iterdir() if d.name.startswith("checkpoint-")],
        key=lambda d: int(d.name.split("-")[-1]),
    )
    return str(checkpoints[-1]) if checkpoints else None


def ensure_dirs(*dirs: str) -> None:
    """Create directories if they don't exist."""
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
