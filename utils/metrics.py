import numpy as np
import cv2
import torch


def to_numpy(img):
    """
    Converts torch tensor or numpy array to numpy (H, W, C) float32
    """
    if isinstance(img, torch.Tensor):
        img = img.detach().cpu().numpy()

    # Handle batch: (N, C, H, W)
    if img.ndim == 4:
        img = img[0]

    # Convert (C, H, W) → (H, W, C)
    if img.shape[0] in [1, 3]:
        img = np.transpose(img, (1, 2, 0))

    return img.astype(np.float32)


def psnr(sr, hr):
    sr = to_numpy(sr)
    hr = to_numpy(hr)

    # Scale if needed
    if sr.max() <= 1.0:
        sr = sr * 255.0
        hr = hr * 255.0

    mse = np.mean((sr - hr) ** 2)
    if mse == 0:
        return float("inf")

    return 20 * np.log10(255.0 / np.sqrt(mse))


def ssim(sr, hr):
    sr = to_numpy(sr)
    hr = to_numpy(hr)

    # Scale if needed
    if sr.max() <= 1.0:
        sr = sr * 255.0
        hr = hr * 255.0

    # ✅ IMPORTANT FIX → use float32 (NOT float64)
    sr = sr.astype(np.float32)
    hr = hr.astype(np.float32)

    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose()).astype(np.float32)

    # Convert to grayscale safely
    if sr.ndim == 3 and sr.shape[2] == 3:
        sr = cv2.cvtColor(sr, cv2.COLOR_RGB2GRAY)
        hr = cv2.cvtColor(hr, cv2.COLOR_RGB2GRAY)

    mu1 = cv2.filter2D(sr, -1, window)[5:-5, 5:-5]
    mu2 = cv2.filter2D(hr, -1, window)[5:-5, 5:-5]

    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = cv2.filter2D(sr ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(hr ** 2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(sr * hr, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / (
        (mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2)
    )

    return ssim_map.mean()