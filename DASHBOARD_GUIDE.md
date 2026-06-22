# 📊 Dashboard Integration Guide

## Overview
A professional, modern web dashboard has been integrated into your Satellite Super-Resolution project. It provides real-time visualization of your model's performance and results.

## ✨ Features

### 1. **Performance Metrics Display**
   - Average PSNR (Peak Signal-to-Noise Ratio)
   - Average SSIM (Structural Similarity Index)
   - Total images processed
   - Model information

### 2. **Interactive Image Gallery**
   - Browse Low-Resolution (LR) images
   - View Super-Resolution (SR) outputs
   - Compare with High-Resolution (HR) ground truth
   - See side-by-side comparisons
   - Navigate with Previous/Next buttons
   - Jump to specific images

### 3. **Project Statistics**
   - Image counts by category
   - Model architecture information
   - Scale factor (4x)
   - Dataset information

### 4. **Responsive Design**
   - Desktop, tablet, and mobile support
   - Beautiful gradient backgrounds
   - Smooth animations and transitions
   - Professional color scheme

## 🚀 Quick Start

### Start the Dashboard

```bash
# Option 1: Using startup script
./start_dashboard.sh

# Option 2: Direct Python
cd dashboard
python3 app.py
```

### Access the Dashboard
Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
Dashboard/
├── start_dashboard.sh          # Startup script
├── dashboard/
│   ├── app.py                  # Flask backend API
│   ├── README.md               # Dashboard documentation
│   ├── templates/
│   │   └── index.html          # Main dashboard HTML
│   └── static/
│       ├── css/
│       │   └── style.css       # Professional styling
│       └── js/
│           └── dashboard.js    # Interactive functionality
└── DASHBOARD_GUIDE.md          # This file
```

## 🔌 API Endpoints

The dashboard uses these REST API endpoints:

### Metrics & Statistics
- `GET /api/metrics` - Get PSNR, SSIM, and image count
- `GET /api/statistics` - Get project statistics
- `GET /api/images` - Get list of all result images

### Image Retrieval
- `GET /api/image/<category>/<filename>` - Get single image
  - Categories: `lr`, `sr`, `hr`, `compare`

### Example:
```bash
# Get metrics
curl http://localhost:5000/api/metrics

# Get an image
curl http://localhost:5000/api/image/sr/sr_0000.png
```

## 📊 How the Dashboard Works

1. **On Load**:
   - Fetches metrics from `results/metrics.json`
   - Loads list of available images
   - Displays statistics

2. **Gallery Navigation**:
   - Browse images by index
   - Previous/Next buttons
   - Direct jump to specific image

3. **Auto-Refresh**:
   - Metrics update every 30 seconds
   - Timestamp shows last update

## 🔄 Integration with Your Workflow

### Step 1: Run Inference
```bash
python3 inference/test.py
```
This generates:
- Images in `results/sr/`, `results/lr/`, `results/hr/`, `results/compare/`
- Metrics in `results/metrics.json`

### Step 2: Start Dashboard
```bash
./start_dashboard.sh
```

### Step 3: View Results
Open browser to `http://localhost:5000`

## 📝 Results Directory Structure

The dashboard expects this directory structure:

```
results/
├── sr/          # Super-resolution images
│   ├── sr_0000.png
│   ├── sr_0001.png
│   └── ...
├── lr/          # Low-resolution images
├── hr/          # High-resolution images
├── compare/     # Comparison images (LR | SR | HR)
└── metrics.json # Metrics file (auto-generated)
```

## 🎨 User Interface Components

### 1. Navigation Bar
- Project title
- Last update timestamp

### 2. Metrics Cards (4 cards)
- PSNR metric with visual icon
- SSIM metric with visual icon
- Total images counter
- Model information

### 3. Statistics Section
- Image counts organized by type
- Project information (dataset, scale, architecture)

### 4. Image Gallery
- Navigation controls (Previous, Next, Go to)
- Image counter display
- 4-image grid layout:
  - LR (top-left)
  - SR (top-right)
  - HR (bottom-left)
  - Comparison (bottom-right, full width)

### 5. Footer
- Dashboard branding
- Version information

## ⚙️ Technical Stack

**Backend:**
- Python 3.7+
- Flask 3.1+
- Standard library modules (json, base64, pathlib)

**Frontend:**
- HTML5
- CSS3 (with Bootstrap 5.3)
- Vanilla JavaScript (ES6+)
- Font Awesome 6.4 (icons)

**Features:**
- REST API architecture
- Base64 image encoding for display
- Responsive design with Bootstrap
- Smooth animations and transitions

## 🔧 Configuration

### Change Dashboard Port

Edit `dashboard/app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Change 5000 to 8080
```

### Custom Styling

Edit `dashboard/static/css/style.css` to customize colors, fonts, and layout.

## 🐛 Troubleshooting

### Issue: "Port 5000 already in use"
```bash
# Find process using port 5000
lsof -i :5000

# Kill it (replace PID with actual number)
kill -9 <PID>
```

### Issue: No images showing
- Verify images exist in `results/` directory
- Check image format is PNG
- Ensure proper directory structure

### Issue: Metrics showing N/A
- Run inference test to generate `metrics.json`
- Check `results/metrics.json` exists
- Verify JSON format is correct

### Issue: Images not loading after refresh
- Check browser console for errors
- Verify image file paths
- Ensure Flask backend is still running

## 📱 Browser Compatibility

- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Advanced Features

### Custom Metrics
Edit `dashboard/app.py` to add custom metrics:

```python
@app.route('/api/custom-metric')
def get_custom_metric():
    return jsonify({'custom_value': 42})
```

### Batch Processing
The dashboard can handle hundreds of result images efficiently.

### Performance Optimization
- Images are served as base64 for immediate display
- Lazy loading prevents memory issues
- Pagination can be added for large datasets

## 📊 Sample Workflow

```bash
# 1. Train/Fine-tune model
python3 training/train.py

# 2. Run inference and generate results
python3 inference/test.py

# 3. Start dashboard to view results
./start_dashboard.sh

# 4. Open browser
# http://localhost:5000

# 5. Navigate through results
# - View metrics
# - Browse images
# - Analyze performance
```

## 🎯 Best Practices

1. **Regular Inference Runs**: Keep running inference to update results
2. **Monitor Metrics**: Check PSNR/SSIM trends over time
3. **Image Analysis**: Use gallery to identify problem cases
4. **Backup Results**: Archive important results before re-running
5. **Browser Caching**: Clear browser cache if images don't update

## 📈 Future Enhancement Ideas

- [ ] Training progress charts
- [ ] Metrics history graphs
- [ ] Model comparison view
- [ ] Batch annotation tools
- [ ] Export as PDF report
- [ ] Dark mode theme
- [ ] Real-time streaming updates
- [ ] Performance benchmarking

## 🔗 Related Files Modified

- `inference/test.py` - Updated to save metrics.json
- `dashboard/app.py` - Flask backend
- `dashboard/templates/index.html` - Dashboard UI
- `dashboard/static/css/style.css` - Styling
- `dashboard/static/js/dashboard.js` - Interactivity

## 📞 Support & Documentation

For more information:
- Check `dashboard/README.md` for API details
- Review inline code comments for implementation details
- Examine `inference/test.py` for metrics generation

---

**Dashboard Version:** 1.0  
**Created:** 2026-05-04  
**Requires:** Python 3.7+, Flask  
**Status:** ✅ Production Ready
