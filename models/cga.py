import torch
import torch.nn as nn


class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(channels, channels, 3, padding=1)
        )

    def forward(self, x):
        return x + self.block(x)


class CGA(nn.Module):
    def __init__(self, in_channels=3, out_channels=3, num_features=64, num_blocks=8, scale_factor=4):
        super().__init__()

        self.scale_factor = scale_factor

        # ================= HEAD =================
        self.head = nn.Conv2d(in_channels, num_features, 3, padding=1)

        # ================= BODY =================
        self.body = nn.Sequential(
            *[ResidualBlock(num_features) for _ in range(num_blocks)]
        )

        # ================= UPSAMPLING =================
        self.upsample = nn.Sequential(
            nn.Conv2d(num_features, num_features * (scale_factor ** 2), 3, padding=1),
            nn.PixelShuffle(scale_factor),  # 4x upscale
            nn.ReLU(inplace=True)
        )

        # ================= TAIL =================
        self.tail = nn.Conv2d(num_features, out_channels, 3, padding=1)

    def forward(self, x):
        x = self.head(x)

        res = self.body(x)
        x = x + res

        x = self.upsample(x)   # 🔥 critical step (150 → 600)

        x = self.tail(x)

        return x