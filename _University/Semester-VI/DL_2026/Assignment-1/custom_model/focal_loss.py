"""
Focal Loss for multi-label classification in YOLO-v8 detection
==============================================================
Paper: "Focal Loss for Dense Object Detection" (Lin et al., ICCV 2017)
https://arxiv.org/abs/1708.02002

Why Focal Loss for CADI-AI?
---------------------------
The training set has a severe class imbalance:
    abiotic  :  1 285 annotations  ( 7%)
    insect   : 11 370 annotations  (62%)
    disease  :  5 626 annotations  (31%)

Focal Loss addresses two orthogonal issues:
1. **Easy-example suppression** (γ > 0): down-weights well-classified
   samples so that hard negatives drive training.
2. **Class-weight rebalancing** (pos_weight): ups the gradient signal for
   the rare 'abiotic' class relative to the dominant 'insect' class.

Focal Loss formula
------------------
    FL(p_t) = -(1 - p_t)^γ · log(p_t)

With α class-weighting (via pos_weight in BCE):
    FL(p_t) = -α_t · (1 - p_t)^γ · log(p_t)

Implementation note
-------------------
Ultralytics v8DetectionLoss uses ``BCEcls`` as its classification loss term.
We replace that nn.BCEWithLogitsLoss with this FocalBCEWithLogitsLoss;
everything else (DFL box regression, IoU loss) remains unchanged.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalBCEWithLogitsLoss(nn.Module):
    """Binary Focal Loss from logits, drop-in replacement for BCEWithLogitsLoss.

    Parameters
    ----------
    gamma       : focusing exponent — 0 recovers standard BCE
    pos_weight  : per-class weight tensor (same length as nc).  Pass None to
                  disable class-weighting.
    reduction   : 'none' | 'mean' | 'sum'  (default 'none' to match Ultralytics)
    """

    def __init__(
        self,
        gamma: float = 2.0,
        pos_weight: torch.Tensor | None = None,
        reduction: str = "none",
    ):
        super().__init__()
        self.gamma = gamma
        self.reduction = reduction
        # pos_weight is registered as a buffer so it moves with the module
        if pos_weight is not None:
            self.register_buffer("pos_weight", pos_weight.float())
        else:
            self.pos_weight = None

    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        Parameters
        ----------
        pred   : (N, nc) raw logits
        target : (N, nc) soft binary targets in [0, 1]
        """
        # Move pos_weight to same device as pred (in case of DDP)
        pw = self.pos_weight.to(pred.device) if self.pos_weight is not None else None

        # Standard BCE loss (stable numerics)
        bce = F.binary_cross_entropy_with_logits(
            pred, target, pos_weight=pw, reduction="none"
        )

        # Focal modulation: down-weight easy examples
        # p_t = sigmoid(pred) when target==1, else 1-sigmoid(pred)
        with torch.no_grad():
            p_t = torch.sigmoid(pred)
            # p_t for positives, 1-p_t for negatives
            p_t = target * p_t + (1.0 - target) * (1.0 - p_t)

        focal_weight = (1.0 - p_t).pow(self.gamma)
        loss = focal_weight * bce

        if self.reduction == "mean":
            return loss.mean()
        elif self.reduction == "sum":
            return loss.sum()
        return loss   # 'none' — Ultralytics sums externally
