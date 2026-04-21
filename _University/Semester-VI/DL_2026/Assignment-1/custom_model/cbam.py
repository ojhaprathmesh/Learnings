"""
CBAM — Convolutional Block Attention Module
============================================
Paper: "CBAM: Convolutional Block Attention Module" (Woo et al., ECCV 2018)
https://arxiv.org/abs/1807.06521

Architecture
------------
Input feature map  →  Channel Attention  →  Spatial Attention  →  Output

Channel Attention  : Squeeze (AvgPool + MaxPool) → Shared MLP → Sigmoid gate
Spatial Attention  : Channel stats (avg + max) → 7×7 conv → Sigmoid gate

Why CBAM for plant stress detection?
- Channel attention forces the backbone to suppress uninformative channels
  (e.g., background soil/sky textures) and amplify channels that encode
  leaf texture, colour anomalies, or insect body features.
- Spatial attention further localises the discriminative regions within
  the feature map — critical for detecting tiny insects (class 1) which
  occupy < 1% of image area.
"""

import torch
import torch.nn as nn


# ---------------------------------------------------------------------------
# Channel Attention
# ---------------------------------------------------------------------------

class ChannelAttention(nn.Module):
    """Squeeze-and-Excitation style channel attention with dual pooling.

    Parameters
    ----------
    channels    : number of input (= output) channels
    reduction   : bottleneck reduction ratio (default 16)
    """

    def __init__(self, channels: int, reduction: int = 16):
        super().__init__()
        mid = max(channels // reduction, 1)
        self.avg_pool = nn.AdaptiveAvgPool2d(1)   # global average pool
        self.max_pool = nn.AdaptiveMaxPool2d(1)    # global max pool

        # Shared MLP (implemented as 1×1 convolutions for efficiency)
        self.mlp = nn.Sequential(
            nn.Conv2d(channels, mid, kernel_size=1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(mid, channels, kernel_size=1, bias=False),
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        avg_feat = self.mlp(self.avg_pool(x))    # (B, C, 1, 1)
        max_feat = self.mlp(self.max_pool(x))    # (B, C, 1, 1)
        gate = self.sigmoid(avg_feat + max_feat) # (B, C, 1, 1)
        return x * gate                          # scale channels


# ---------------------------------------------------------------------------
# Spatial Attention
# ---------------------------------------------------------------------------

class SpatialAttention(nn.Module):
    """Spatial attention based on channel-pooled statistics.

    Parameters
    ----------
    kernel_size : conv kernel size (paper suggests 7 for larger receptive field)
    """

    def __init__(self, kernel_size: int = 7):
        super().__init__()
        assert kernel_size % 2 == 1, "kernel_size must be odd"
        self.conv = nn.Conv2d(
            2, 1,
            kernel_size=kernel_size,
            padding=kernel_size // 2,
            bias=False,
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        avg_map = x.mean(dim=1, keepdim=True)        # (B, 1, H, W) channel avg
        max_map = x.max(dim=1, keepdim=True).values  # (B, 1, H, W) channel max
        spatial = torch.cat([avg_map, max_map], dim=1)  # (B, 2, H, W)
        gate = self.sigmoid(self.conv(spatial))          # (B, 1, H, W)
        return x * gate                                  # scale spatially


# ---------------------------------------------------------------------------
# CBAM — combined module (Ultralytics-compatible)
# ---------------------------------------------------------------------------

class CBAM(nn.Module):
    """Combined Channel + Spatial Attention for Ultralytics YOLO integration.

    Ultralytics YAML usage
    ----------------------
    In the YAML architecture file, specify the output-channel count as the
    sole argument (same as input channels since CBAM is a passthrough w.r.t.
    channel dimension):

        - [-1, 1, CBAM, [64]]    # 64-channel feature map

    The Ultralytics parse_model function handles unknown modules by setting
    c2 = c1 (passthrough) and calling ``CBAM(64)``.

    Parameters
    ----------
    channels    : input (= output) channel count
    reduction   : channel-attention bottleneck ratio  (default 16)
    kernel_size : spatial-attention conv kernel size  (default 7)
    """

    def __init__(self, channels: int, reduction: int = 16, kernel_size: int = 7):
        super().__init__()
        self.channel_attention = ChannelAttention(channels, reduction)
        self.spatial_attention = SpatialAttention(kernel_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.channel_attention(x)
        x = self.spatial_attention(x)
        return x
