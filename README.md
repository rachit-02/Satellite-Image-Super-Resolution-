<div align="center">

# 🛰️ CGA: Curvature-Guided Attention for Remote Sensing Image Super-Resolution

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-1.9+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge" />
</p>

<p align="center">
  <strong>Official implementation of the paper:<br>
  "CGA: Curvature-Guided Attention for Remote Sensing Image Super-Resolution"</strong>
</p>

<p align="center">
  <a href="https://satellite-image-super-resolution.onrender.com/">🌐 Live Demo</a> •
  <a href="#-results">📊 Results</a> •
  <a href="#-installation">🚀 Installation</a> •
  <a href="#-datasets">📦 Datasets</a> •
  <a href="#-interactive-dashboard">🎨 Dashboard</a> •
  <a href="#-model-architecture">🧠 Architecture</a>
</p>

<p align="center">
  <a href="https://satellite-image-super-resolution.onrender.com/">
    <img src="https://img.shields.io/badge/🚀 Try Live Demo-satellite--image--super--resolution.onrender.com-blue?style=for-the-badge" />
  </a>
</p>

</div>

---

## 📋 Overview

**CGA (Curvature-Guided Attention)** is a deep learning architecture specifically designed for **4× super-resolution of satellite and remote sensing imagery**. By leveraging geometric curvature information to guide spatial attention, CGA preserves fine structural details — roads, building edges, and vegetation boundaries — that conventional SR methods tend to blur.

### Why CGA?

| Problem | CGA Solution |
|---|---|
| Existing SR models ignore geometric structure | Curvature map guides attention to edges & boundaries |
| Generic SR degrades satellite-specific features | Trained on remote sensing datasets (AID, UCMerced, WHU-RS19) |
| Expensive high-res satellite sensors | 4× enhancement from cheap low-res imagery |
| Slow per-image processing | ~50ms/image inference on GPU |

---

## ✨ Key Features

- **🔬 Curvature-Guided Attention** — novel mechanism that computes local surface curvature to preserve edges
- **4× Super-Resolution** — 64×64 → 256×256 with PSNR 27.56 dB / SSIM 0.7365
- **Multi-dataset evaluation** — AID, UCMerced, WHU-RS19 benchmarks
- **Interactive Dashboard** — [live web UI](https://satellite-image-super-resolution.onrender.com/) for side-by-side comparisons
- **Lightweight** — only ~1.3M parameters (~5 MB checkpoint)
- **Easy integration** — clean Python API, pre-trained checkpoints included

---

## 📊 Results

### Quantitative Performance

| Metric | Score | Note |
|--------|-------|------|
| **PSNR** | **27.56 dB** | Higher is better |
| **SSIM** | **0.7365** | Scale 0–1 |
| **Scale Factor** | 4× | 64×64 → 256×256 |
| **Test Images** | 2,190+ | Across three datasets |
| **Inference Speed** | ~50 ms/img | GPU (CUDA) |

### Visual Comparison

```
Low-Resolution Input (64×64)   →   CGA Output (256×256)   →   Ground Truth (256×256)
       ┌──────────┐                  ┌──────────────────┐       ┌──────────────────┐
       │  Blurry  │   ─── CGA ───►  │  Sharp + Detail  │  ≈    │    Reference     │
       │ ░░░░░░░░ │                  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │       │  ████████████  │
       └──────────┘                  └──────────────────┘       └──────────────────┘
```

> 🌐 **See live comparisons:** [satellite-image-super-resolution.onrender.com](https://satellite-image-super-resolution.onrender.com/)

---

## 📦 Datasets

Training and testing sets used in this work can be downloaded as follows.

### 🗂️ AID Dataset

| Split | Download | Size |
|-------|----------|------|
| Training + Validation | [Baidu Drive](https://pan.baidu.com) `password: id1n` · [Google Drive](https://drive.google.com) | 7850 train / 150 val |
| Test Set | [Baidu Drive](https://pan.baidu.com) `password: id1n` · [Google Drive](https://drive.google.com) | 2000 images |

### 🗂️ UCMerced Dataset

| Split | Download | Size |
|-------|----------|------|
| Test Set | [Baidu Drive](https://pan.baidu.com) `password: terr` · [Google Drive](https://drive.google.com) | 1050 images |

### 🗂️ WHU-RS19 Dataset

| Split | Download | Size |
|-------|----------|------|
| Test Set | [Baidu Drive](https://pan.baidu.com) `password: ol6j` | 1002 images |

### Dataset Setup

After downloading, place all datasets into the `datasets/` directory following the structure below:

```
datasets/
├── AID/
│   ├── train/
│   ├── val/
│   └── test/
├── UCMerced/
│   └── test/
└── WHU-RS19/
    └── test/
```

> See [datasets/README.md](datasets/README.md) for the complete directory structure and preprocessing steps.

---

## 🎨 Interactive Dashboard

The project includes a **live web dashboard** for browsing and comparing model outputs.

**🔗 Live:** [satellite-image-super-resolution.onrender.com](https://satellite-image-super-resolution.onrender.com/)

![Satellite SR Dashboard](assets/dashboard_preview.png)

**Dashboard features:**

- 📊 Real-time PSNR / SSIM metrics display
- 🖼️ Side-by-side LR / SR / HR image gallery (50 examples)
- 🔢 Jump-to-image navigation
- 📥 Download images directly from the UI
- 📱 Fully responsive on desktop, tablet, and mobile
- ⚡ Smooth animations with professional dark UI

**Run locally:**
```bash
./start_dashboard.sh
# Open: http://localhost:5000
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- CUDA 11.0+ *(optional, for GPU acceleration)*
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/mwaleedaslam/CGA.git
cd CGA

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify setup
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
```

---

## 💻 Usage

### Inference

```bash
# Run on test set (uses checkpoints/best_model.pth)
python inference/test.py

# GPU selection (optional)
CUDA_VISIBLE_DEVICES=0 python inference/test.py
```

### Python API

```python
import torch
from models.cga import CGA

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load pre-trained model
model = CGA(in_channels=3, num_features=64, num_blocks=8, scale_factor=4)
model.load_state_dict(torch.load('checkpoints/best_model.pth', map_location=device))
model = model.to(device).eval()

# Super-resolve a low-resolution patch
with torch.no_grad():
    lr = torch.randn(1, 3, 64, 64).to(device)   # replace with real image tensor
    sr = model(lr)
    print(f"LR: {lr.shape}  →  SR: {sr.shape}")
# LR: torch.Size([1, 3, 64, 64])  →  SR: torch.Size([1, 3, 256, 256])
```

### Training

```bash
# Standard training (100 epochs)
python training/train.py

# Extended training (150 epochs)
python training/train_150.py
```

---

## 🧠 Model Architecture

![CGA Architecture Overview](assets/cga_architecture.png)

> *LR input → 3×3 Conv → LCGA Blocks × n → CGTA Blocks × m → Conv → HR output*

The pipeline takes a **Low-Resolution (LR)** satellite image and passes it through a 3×3 Conv stem, then a stack of **Curvature-Guided Attention Blocks**, and a final reconstruction Conv to produce the **High-Resolution (HR)** output. Two complementary mechanisms power the blocks:

**A. LCGA — Local Curvature-Guided Attention**
Operates on local windows. Estimates a curvature map per window (highlighting edges and curves) and uses it to weight attention — strengthening continuity of roads, rivers, and buildings while suppressing flat uninformative regions.

**B. CGTA — Curvature-Guided Token Attention**
Operates globally across all windows. Curvature scores select only the most informative tokens; global attention runs solely on those tokens, capturing long-range structural dependencies at near-linear complexity.

| Component | Details |
|-----------|---------|
| Parameters | ~1.3 M |
| Model size | ~5 MB |
| Scale factor | 4× |
| Input size | 64×64 px |
| Output size | 256×256 px |
| Inference (GPU) | ~50 ms/image |

---

## 📁 Project Structure

```
CGA/
├── models/
│   └── cga.py                    # CGA network architecture
├── training/
│   ├── train.py                  # 100-epoch training script
│   └── train_150.py              # Extended 150-epoch training
├── inference/
│   └── test.py                   # Inference & evaluation
├── configs/
│   ├── config.py                 # Default hyperparameters
│   └── config_150.py             # 150-epoch config
├── utils/
│   ├── dataloader.py             # Dataset loading
│   ├── metrics.py                # PSNR / SSIM computation
│   ├── image_utils.py            # Image I/O helpers
│   └── preprocessing.py         # Augmentation & preprocessing
├── dashboard/
│   ├── app.py                    # Flask backend
│   ├── templates/index_modern.html
│   └── static/                  # CSS / JS
├── checkpoints/
│   ├── best_model.pth            # Best checkpoint
│   └── last_model.pth            # Latest checkpoint
├── results/
│   ├── metrics.json              # Evaluation metrics
│   ├── lr/                       # 50 LR test images
│   ├── sr/                       # 50 SR outputs
│   ├── hr/                       # 50 HR ground truth
│   └── compare/                  # Side-by-side comparisons
├── datasets/                     # Place downloaded data here
├── requirements.txt
├── start_dashboard.sh
└── README.md
```

---

## ⚙️ Configuration

### Training (`configs/config.py`)

```python
config = {
    'model': {
        'in_channels': 3,
        'num_features': 64,
        'num_blocks': 8,
        'scale_factor': 4
    },
    'training': {
        'epochs': 100,
        'batch_size': 32,
        'learning_rate': 1e-3,
        'optimizer': 'Adam'
    },
    'data': {
        'train_split': 0.8,
        'val_split': 0.1,
        'test_split': 0.1
    }
}
```

---

## 🔌 REST API

The dashboard exposes a simple JSON API for programmatic access:

```
GET /api/metrics      → { "psnr": 27.56, "ssim": 0.7365, "total_images": 2190, ... }
GET /api/statistics   → { "model_name": "CGA", "scale_factor": "4x", ... }
GET /api/images       → [ { "name": "image_1", "lr": "...", "sr": "...", "hr": "..." }, ... ]
GET /api/image-file/<category>/<filename>   # category: lr | sr | hr | compare
```

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| `CUDA out of memory` | Reduce `batch_size` to 16, or set `CUDA_VISIBLE_DEVICES=""` for CPU |
| `ModuleNotFoundError` | Run `pip install --upgrade -r requirements.txt` |
| Dashboard won't start | Check `lsof -i :5000`; change `PORT` in `dashboard/app.py` if occupied |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo and create a feature branch (`git checkout -b feature/my-feature`)
2. Commit changes with a clear message
3. Open a Pull Request describing what you changed and why

Areas of interest: model improvements, new benchmark datasets, UI enhancements, documentation.

---

## 📋 Requirements

```
torch>=1.9.0
torchvision>=0.10.0
flask>=2.0.0
flask-cors>=3.0.0
numpy>=1.19.0
opencv-python>=4.5.0
scikit-image>=0.18.0
Pillow>=8.0.0
```

---

## 📝 Citation

If you use this work, please cite:

```bibtex
@article{cga2024,
  title   = {CGA: Curvature-Guided Attention for Remote Sensing Image Super-Resolution},
  author  = {Waleed Aslam, M. and et al.},
  year    = {2024},
  url     = {https://github.com/mwaleedaslam/CGA}
}
```

---

## 📄 License

Released under the [MIT License](LICENSE).
