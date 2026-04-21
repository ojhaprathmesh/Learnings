"""
Transformer Neck Block
======================
A lightweight multi-head self-attention (MHSA) block inserted at the
bottleneck of the feature pyramid neck (after SPPF).

Motivation
----------
Standard YOLO necks rely purely on convolutional operations with limited
receptive fields.  Insects and disease lesions can appear in clusters
scattered across the image, requiring *long-range* context.  A single
MHSA block at the lowest-resolution feature map (stride-32, 20×20 tokens
for 640×640 input) captures global dependencies at negligible extra cost:

    Parameters added ≈ 4 × 256² (MHSA) + 2 × 256 × 1024 (FFN) ≈ 786 k
    vs. YOLOv8n total ≈ 3.1 M  →  adds ~25 % parameter overhead.

Architecture (Pre-LN Transformer encoder layer)
-----------------------------------------------
Input (B, C, H, W)
  → flatten to (B, H×W, C) token sequence
  → LayerNorm → MHSA → residual
  → LayerNorm → FFN (Linear-GELU-Linear) → residual
  → reshape to (B, C, H, W)
"""

import torch
import torch.nn as nn


class TransformerNeck(nn.Module):
    """Single Pre-LayerNorm Transformer encoder layer for YOLO neck.

    Ultralytics YAML usage
    ----------------------
        - [-1, 1, TransformerNeck, [256]]   # 256-channel SPPF output

    The module is a spatial passthrough (H, W, and C unchanged); only the
    feature values are updated via self-attention + feed-forward.

    Parameters
    ----------
    channels  : number of feature channels (= embed_dim for MHSA)
    num_heads : number of self-attention heads (default 4)
    mlp_ratio : FFN hidden-dim expansion factor (default 4)
    dropout   : attention & FFN dropout probability (default 0.0)
    """

    def __init__(
        self,
        channels: int,
        num_heads: int = 4,
        mlp_ratio: int = 4,
        dropout: float = 0.0,
    ):
        super().__init__()
        assert channels % num_heads == 0, (
            f"channels ({channels}) must be divisible by num_heads ({num_heads})"
        )
        hidden_dim = channels * mlp_ratio

        # Pre-LN self-attention
        self.norm1 = nn.LayerNorm(channels)
        self.attn = nn.MultiheadAttention(
            embed_dim=channels,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True,
        )
        self.attn_drop = nn.Dropout(dropout)

        # Pre-LN feed-forward network
        self.norm2 = nn.LayerNorm(channels)
        self.ffn = nn.Sequential(
            nn.Linear(channels, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, channels),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, C, H, W = x.shape

        # Flatten spatial dims → token sequence  (B, N, C) where N = H × W
        tokens = x.flatten(2).permute(0, 2, 1)   # (B, H*W, C)

        # --- Self-attention sub-layer (Pre-LN + residual) ---
        normed = self.norm1(tokens)
        attn_out, _ = self.attn(normed, normed, normed)
        tokens = tokens + self.attn_drop(attn_out)

        # --- FFN sub-layer (Pre-LN + residual) ---
        tokens = tokens + self.ffn(self.norm2(tokens))

        # Reshape back to spatial tensor
        out = tokens.permute(0, 2, 1).reshape(B, C, H, W)
        return out
