"""
YOLO-TRP Custom Trainer
========================
Subclasses Ultralytics DetectionTrainer to:
1. Register CBAM and TransformerNeck into Ultralytics' model-parsing namespace.
2. Replace BCEcls with FocalBCEWithLogitsLoss (γ=2, class-weighted).

Usage
-----
    from custom_model.yolo_trp_trainer import YOLOTRPTrainer
    from pathlib import Path

    trainer = YOLOTRPTrainer(overrides={
        "model": "custom_model/yolo_trp.yaml",
        "data":  "dataset.yaml",
        "epochs": 32,
        ...
    })
    trainer.train()
"""

import sys
import torch
import torch.nn as nn
from pathlib import Path
from copy import deepcopy

from ultralytics.models.yolo.detect import DetectionTrainer
from ultralytics.utils.loss import v8DetectionLoss

from .cbam import CBAM
from .transformer_neck import TransformerNeck
from .focal_loss import FocalBCEWithLogitsLoss


# ---------------------------------------------------------------------------
# Class-balancing weights computed from training-set annotation counts
#   abiotic : 1 285  →  (11370 / 1285) ≈ 8.85
#   insect  : 11 370 →  1.00  (most frequent, reference)
#   disease :  5 626 →  (11370 / 5626) ≈ 2.02
# ---------------------------------------------------------------------------
_CLASS_WEIGHTS = torch.tensor([8.85, 1.00, 2.02])


# ---------------------------------------------------------------------------
# Custom Detection Loss (replaces BCEcls with Focal Loss)
# ---------------------------------------------------------------------------

class YOLOTRPLoss(v8DetectionLoss):
    """v8DetectionLoss with focal BCE classification loss.

    Parameters
    ----------
    model         : the detection model (passed to super().__init__)
    class_weights : 1-D tensor of length nc with per-class pos_weights
    gamma         : focal exponent (default 2.0)
    """

    def __init__(
        self,
        model: nn.Module,
        class_weights: torch.Tensor = _CLASS_WEIGHTS,
        gamma: float = 2.0,
    ):
        super().__init__(model)
        # Replace the classification BCE with focal loss
        self.BCEcls = FocalBCEWithLogitsLoss(gamma=gamma, pos_weight=class_weights)


# ---------------------------------------------------------------------------
# Custom Trainer
# ---------------------------------------------------------------------------

class YOLOTRPTrainer(DetectionTrainer):
    """Ultralytics DetectionTrainer subclass that:
    - Registers CBAM / TransformerNeck in the YOLO model parser globals.
    - Uses YOLOTRPLoss (focal BC E + class weights) instead of standard loss.
    """

    # ------------------------------------------------------------------
    # Step 1: register custom modules BEFORE any model is parsed
    # ------------------------------------------------------------------
    @staticmethod
    def _register_custom_modules() -> None:
        """Inject CBAM and TransformerNeck into Ultralytics' parser scope."""
        import ultralytics.nn.tasks as _tasks

        _tasks.CBAM = CBAM                        # type: ignore[attr-defined]
        _tasks.TransformerNeck = TransformerNeck  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    # Step 2: build model (called by Ultralytics training loop)
    # ------------------------------------------------------------------
    def get_model(self, cfg=None, weights=None, verbose: bool = True):
        self._register_custom_modules()
        return super().get_model(cfg=cfg, weights=weights, verbose=verbose)

    # ------------------------------------------------------------------
    # Step 3: swap in the focal-loss criterion
    # ------------------------------------------------------------------
    def init_criterion(self) -> YOLOTRPLoss:
        return YOLOTRPLoss(self.model)
