# 🛰️ Satellite Super-Resolution with Curvature-Guided Attention (CGA)

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.9+-red.svg?style=flat-square)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

**A deep learning model for 4x satellite image super-resolution with interactive web dashboard**

[Features](#-key-features) • [Results](#-results) • [Installation](#-installation) • [Dashboard](#-interactive-dashboard) • [Docs](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Results & Performance](#-results--performance)
- [Interactive Dashboard](#-interactive-dashboard)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Model Architecture](#-model-architecture)
- [Results Showcase](#-results-showcase)
- [Documentation](#-documentation)
- [Contributing](#-contributing)

---

## 🎯 Overview

**Satellite Super-Resolution** is a state-of-the-art deep learning project that enhances low-resolution satellite imagery to high-resolution using a **Curvature-Guided Attention (CGA)** neural network. The model achieves **4x upscaling** with exceptional quality, making it perfect for remote sensing, urban planning, agricultural monitoring, and environmental analysis.

### Why This Matters 🌍
- **Cost Reduction**: Higher resolution without expensive satellite sensors
- **Better Analysis**: Enhanced details for improved decision-making
- **Accessibility**: Make satellite data usable for more applications
- **Speed**: Process thousands of images quickly with GPU acceleration

---

## ✨ Key Features

| Feature | Details |
|---------|---------|
| **🚀 Advanced Architecture** | Curvature-Guided Attention (CGA) with residual learning |
| **🔄 4x Upscaling** | 64×64 → 256×256 pixel satellite images |
| **📊 Performance Metrics** | PSNR: **27.56 dB** | SSIM: **0.7365** |
| **🎨 Interactive Dashboard** | Web-based UI for visualizing results in real-time |
| **📈 Batch Processing** | Process 2,190+ satellite images efficiently |
| **💾 Pre-trained Models** | Ready-to-use checkpoints for immediate inference |
| **🔧 Easy Integration** | Simple API for deployment and integration |
| **📱 Responsive UI** | Desktop, tablet, and mobile compatible |

---

## 📊 Results & Performance

### Performance Metrics
```
┌─────────────────────────────────────┐
│  Performance on Test Dataset        │
├─────────────────────────────────────┤
│ PSNR (Peak Signal-to-Noise Ratio): │
│   → 27.56 dB (Higher is better)    │
│                                     │
│ SSIM (Structural Similarity):      │
│   → 0.7365 (Scale 0-1)             │
│                                     │
│ Total Images Processed:             │
│   → 2,190+ satellite images        │
│                                     │
│ Upscaling Factor: 4x                │
│   → 64×64 → 256×256 pixels         │
└─────────────────────────────────────┘
```

### Image Results Example
```
Input (LR)          →  Model Output (SR)  →  Ground Truth (HR)
┌──────────┐       ┌────────────────┐   ┌────────────────┐
│ 64×64    │  CGA  │ 256×256        │   │ 256×256        │
│ ░░░░░░░░ │ ────→ │ ▒▒▒▒▒▒▒▒▒▒▒▒   │   │ ████████████   │
│ ░░░░░░░░ │       │ ▒▒▒▒▒▒▒▒▒▒▒▒   │   │ ████████████   │
└──────────┘       └────────────────┘   └────────────────┘
  Blurry              Enhanced Detail      Reference
```

---

## 🎨 Interactive Dashboard

### Live Dashboard Preview
The project includes a **professional web dashboard** for visualizing results:

**Features:**
- ✅ **Real-time Metrics Display** - PSNR, SSIM, image counts
- ✅ **Interactive Image Gallery** - Browse LR, SR, HR, and comparison images
- ✅ **Image Navigation** - Jump to specific images or browse sequentially
- ✅ **Project Statistics** - Model info, scale factor, dataset type
- ✅ **Professional UI** - Modern design with smooth animations
- ✅ **Responsive Layout** - Works perfectly on all devices

### Dashboard Sections
```
┌─────────────────────────────────────────────────────┐
│  Satellite SR Dashboard  [● Live]                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ◄ Metrics  │ ■ Gallery ■ │  About CGA  │          │
│                                                      │
│  📊 PERFORMANCE METRICS                             │
│  ┌──────────────┬──────────────┬──────────────┐     │
│  │ PSNR: 27.56  │ SSIM: 0.7365 │ Images: 50   │     │
│  │     dB       │    Score     │  Processed   │     │
│  └──────────────┴──────────────┴──────────────┘     │
│                                                      │
│  🖼️  IMAGE COMPARISON                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │    LR    │  │    SR    │  │    HR    │         │
│  │ 64×64    │  │ 256×256  │  │ 256×256  │         │
│  └──────────┘  └──────────┘  └──────────┘         │
│                                                      │
│         ◀ Previous  [1] Jump  Next ▶               │
│         Image 1 of 50                              │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Start Dashboard:**
```bash
./start_dashboard.sh
# Open: http://localhost:5000
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- CUDA 11.0+ (for GPU support, optional but recommended)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/satellite-super-resolution.git
cd satellite-super-resolution
```

### Step 2: Create Virtual Environment
```bash
# Using venv
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import flask; print(f'Flask: {flask.__version__}')"
```

---

## 💻 Usage

### Quick Start - Run Inference
```bash
# Process satellite images and generate super-resolution outputs
python inference/test.py

# Run on specific GPU (optional)
CUDA_VISIBLE_DEVICES=0 python inference/test.py
```

### Start Interactive Dashboard
```bash
# Option 1: Using startup script
./start_dashboard.sh

# Option 2: Manual start
python dashboard/app.py
```

Then open your browser: **http://localhost:5000**

### Use Pre-trained Model
```python
import torch
from models.cga import CGA

# Load model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CGA(in_channels=3, num_features=64, num_blocks=8, scale_factor=4)
model.load_state_dict(torch.load('checkpoints/best_model.pth'))
model = model.to(device)
model.eval()

# Inference on image
with torch.no_grad():
    lr_image = torch.randn(1, 3, 64, 64).to(device)
    sr_image = model(lr_image)
    print(f"Input: {lr_image.shape} → Output: {sr_image.shape}")
```

### Train Your Own Model
```bash
# Configure training in configs/config.py
# Then run:
python training/train.py

# Or with 150 epochs:
python training/train_150.py
```

---

## 📁 Project Structure

```
satellite-super-resolution/
│
├── 🎨 dashboard/                    # Web dashboard
│   ├── app.py                       # Flask backend API
│   ├── README.md                    # Dashboard documentation
│   ├── templates/
│   │   └── index_modern.html        # Modern UI template
│   └── static/
│       ├── css/
│       │   └── style.css            # Dashboard styles
│       └── js/
│           └── dashboard.js         # Interactive scripts
│
├── 🧠 models/
│   └── cga.py                       # CGA model architecture
│
├── 🔄 training/
│   ├── train.py                     # Training script
│   └── train_150.py                 # Extended training (150 epochs)
│
├── 🧪 inference/
│   └── test.py                      # Inference/testing script
│
├── ⚙️ configs/
│   ├── config.py                    # Default configuration
│   └── config_150.py                # Configuration for 150 epochs
│
├── 🛠️ utils/
│   ├── dataloader.py                # Data loading utilities
│   ├── metrics.py                   # Performance metrics
│   ├── image_utils.py               # Image processing
│   └── preprocessing.py             # Data preprocessing
│
├── 💾 checkpoints/
│   ├── best_model.pth               # Best trained model
│   └── last_model.pth               # Last checkpoint
│
├── 📊 results/
│   ├── metrics.json                 # Performance metrics
│   ├── lr/                          # Low-resolution inputs (50 images)
│   ├── sr/                          # Super-resolution outputs (50 images)
│   ├── hr/                          # High-resolution ground truth (50 images)
│   └── compare/                     # Side-by-side comparisons (50 images)
│
├── 📈 logs/                         # Training logs
├── 📚 experiments/                  # Experiment results
│
├── 📖 Documentation
│   ├── README.md                    # This file
│   ├── GETTING_STARTED.md           # Quick start guide
│   ├── DASHBOARD_GUIDE.md           # Dashboard documentation
│   ├── DASHBOARD_UI_GUIDE.md        # UI design documentation
│   └── DASHBOARD_IMPLEMENTATION_SUMMARY.md
│
├── requirements.txt                 # Python dependencies
├── start_dashboard.sh               # Dashboard startup script
└── User-Guide HPC.pdf               # HPC usage guide
```

---

## 🧠 Model Architecture

### Curvature-Guided Attention (CGA) Network

```
Input (LR Image)
      ↓
   ┌──────────────────────┐
   │  Head Conv (3→64)    │
   └──────────┬───────────┘
              ↓
   ┌──────────────────────┐
   │ Residual Blocks × 8  │  ← CGA mechanism
   │ (Skip connections)   │
   └──────────┬───────────┘
              ↓
   ┌──────────────────────┐
   │ Pixel Shuffle (4x)   │
   │ 64 → 256 features    │
   └──────────┬───────────┘
              ↓
   ┌──────────────────────┐
   │  Tail Conv (64→3)    │
   └──────────┬───────────┘
              ↓
Output (SR Image)
```

### Key Components
- **Head**: Initial feature extraction (Conv2D)
- **Body**: 8 residual blocks with skip connections
- **Upsampler**: Pixel shuffling for 4x super-resolution
- **Tail**: Final reconstruction layer
- **Attention**: Curvature guidance for edge preservation

### Model Specifications
```
Total Parameters: ~1.3M
Trainable Params: 1.3M
Model Size: ~5 MB
Inference Time: ~50ms per image (GPU)
```

---

## 📸 Results Showcase

### Visual Results

**Example 1: Urban Area**
```
LR Input (Blurry)    →  CGA Output (Enhanced)   →  Ground Truth (Reference)
```

**Example 2: Agricultural Land**
```
LR Input (Blurry)    →  CGA Output (Enhanced)   →  Ground Truth (Reference)
```

### Sample Output Structure
Results are organized in the `results/` folder:

| Folder | Description | Count |
|--------|-------------|-------|
| `results/lr/` | Low-resolution inputs (64×64) | 50 |
| `results/sr/` | Model outputs (256×256) | 50 |
| `results/hr/` | Ground truth references (256×256) | 50 |
| `results/compare/` | Side-by-side comparisons | 50 |

---

## 📚 Documentation

### Complete Documentation Files

1. **[GETTING_STARTED.md](GETTING_STARTED.md)** ⭐ **START HERE**
   - 60-second quick start
   - Common tasks & troubleshooting
   - FAQ and pro tips

2. **[DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md)**
   - Complete feature documentation
   - Workflow integration
   - Advanced configuration

3. **[DASHBOARD_UI_GUIDE.md](DASHBOARD_UI_GUIDE.md)**
   - Visual layout preview
   - Color scheme & design
   - Interactive elements

4. **[dashboard/README.md](dashboard/README.md)**
   - API endpoint reference
   - Backend structure
   - Integration guide

5. **[QUICK_START_DASHBOARD.md](QUICK_START_DASHBOARD.md)**
   - Quick reference
   - API overview
   - Common operations

---

## 🔧 Configuration

### Training Configuration (configs/config.py)
```python
{
    'model': {
        'in_channels': 3,
        'num_features': 64,
        'num_blocks': 8,
        'scale_factor': 4
    },
    'training': {
        'epochs': 100,
        'batch_size': 32,
        'learning_rate': 0.001,
        'optimizer': 'Adam'
    },
    'data': {
        'dataset': 'Satellite Images',
        'train_split': 0.8,
        'val_split': 0.1,
        'test_split': 0.1
    }
}
```

### Dashboard Configuration (dashboard/app.py)
```python
PORT = 5000
DEBUG = True
RESULTS_DIR = 'results/'
METRICS_FILE = 'results/metrics.json'
```

---

## 📊 API Reference

### Dashboard API Endpoints

```bash
# Get performance metrics
GET /api/metrics
Response: {
    "psnr": 27.56,
    "ssim": 0.7365,
    "total_images": 2190,
    "last_updated": "2026-05-04 14:54:50"
}

# Get project statistics
GET /api/statistics
Response: {
    "model_name": "CGA",
    "scale_factor": "4x",
    "dataset": "Satellite Images",
    "lr_count": 50,
    "sr_count": 50,
    "hr_count": 50,
    "compare_count": 50
}

# Get all images
GET /api/images
Response: [
    {
        "name": "image_1",
        "lr": "/api/image-file/lr/image_1.png",
        "sr": "/api/image-file/sr/image_1.png",
        ...
    }
]

# Get specific image
GET /api/image-file/<category>/<filename>
Categories: lr, sr, hr, compare
```

---

## 🎓 Training & Evaluation

### Train Model
```bash
# Standard training (100 epochs)
python training/train.py

# Extended training (150 epochs)
python training/train_150.py

# Monitor with dashboard
# In another terminal:
./start_dashboard.sh
```

### Evaluate Results
```bash
# Run inference on test set
python inference/test.py

# View metrics
cat results/metrics.json

# Visualize results
# Open dashboard: http://localhost:5000
```

---

## 🚀 Performance Optimization

### GPU Acceleration
```bash
# Enable CUDA
export CUDA_VISIBLE_DEVICES=0

# Multi-GPU training
export CUDA_VISIBLE_DEVICES=0,1
python training/train.py
```

### Memory Optimization
```python
# Reduce batch size if OOM
batch_size = 16  # instead of 32

# Use mixed precision
from torch.cuda.amp import autocast
with autocast():
    output = model(input)
```

### Speed Tips
- Use GPU for inference (~50ms per image)
- Batch processing for multiple images
- Enable cudnn benchmarking
- Use mixed precision training

---

## 🐛 Troubleshooting

### Issue: "CUDA out of memory"
```bash
# Reduce batch size in config
batch_size = 16
# Or use CPU
export CUDA_VISIBLE_DEVICES=""
```

### Issue: "Module not found"
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: "Dashboard won't start"
```bash
# Check port availability
lsof -i :5000
# Try different port in dashboard/app.py
PORT = 5001
```

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Areas to Contribute
- 🎨 UI/Dashboard improvements
- 📈 Model architecture enhancements
- 📊 Performance optimizations
- 📚 Documentation improvements
- 🐛 Bug fixes and testing

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

Full list in [requirements.txt](requirements.txt)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**Project Team:**
- Nimit Rachit
- Dhananjay
- Sushil Ghildiyal

---

## 🙏 Acknowledgments

- PyTorch team for the amazing framework
- Flask community for web framework
- Dataset providers for satellite imagery
- Contributors and users for feedback

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/satellite-super-resolution/issues)
- **Email**: your.email@example.com
- **Documentation**: See [GETTING_STARTED.md](GETTING_STARTED.md)

---

## 📈 Project Status

- ✅ Model training & inference
- ✅ Interactive dashboard
- ✅ API endpoints
- ✅ Performance metrics
- ✅ Documentation
- 🔄 Continuous improvements
- 🚀 Future: Real-time processing, Mobile app

---

<div align="center">

**⭐ If you find this project helpful, please consider starring it! ⭐**

Made with ❤️ for satellite imagery enhancement

</div>
