# 📊 Satellite Super-Resolution Dashboard

A professional, interactive web-based dashboard for visualizing satellite super-resolution results and metrics.

## Features

✨ **Key Features:**
- **Real-time Metrics Display** - Shows PSNR and SSIM performance metrics
- **Interactive Image Gallery** - Browse through LR, SR, HR, and comparison images
- **Image Navigation** - Jump to specific images or browse sequentially
- **Statistics Dashboard** - View project information and image counts
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **Professional UI** - Clean, modern interface with beautiful visualizations

## Quick Start

### Option 1: Using the startup script
```bash
./start_dashboard.sh
```

### Option 2: Manual startup
```bash
cd dashboard
python3 app.py
```

The dashboard will be available at: **http://localhost:5000**

## API Endpoints

The dashboard includes a REST API for accessing project data:

- `GET /` - Main dashboard page
- `GET /api/metrics` - Get overall PSNR and SSIM metrics
- `GET /api/statistics` - Get project statistics
- `GET /api/images` - Get list of all result images
- `GET /api/image/<category>/<filename>` - Get a specific image
- `GET /api/sample-comparison/<idx>` - Get a comparison set

### Supported Categories:
- `lr` - Low-Resolution images
- `sr` - Super-Resolution images (model output)
- `hr` - High-Resolution images (ground truth)
- `compare` - Side-by-side comparison images

## Project Structure

```
dashboard/
├── app.py                 # Flask backend application
├── templates/
│   └── index.html        # Main dashboard HTML
└── static/
    ├── css/
    │   └── style.css     # Dashboard styling
    └── js/
        └── dashboard.js  # Dashboard functionality
```

## Requirements

- Python 3.7+
- Flask (automatically installed with requirements)

Install dependencies:
```bash
pip install Flask
```

## Technical Details

**Backend:** Flask (lightweight Python web framework)
**Frontend:** HTML5, CSS3, JavaScript (ES6+)
**Styling:** Bootstrap 5.3 + Custom CSS
**Image Format:** PNG
**Metrics Supported:** PSNR, SSIM

## How It Works

1. **Metrics Loading**: The dashboard automatically reads PSNR and SSIM values from test results
2. **Image Gallery**: Displays all generated images organized by category
3. **Navigation**: Browse through results with previous/next buttons or jump to specific images
4. **Auto-refresh**: Metrics automatically update every 30 seconds

## Results Directory Structure

The dashboard expects results in the following structure:
```
results/
├── sr/      # Super-resolution images
├── lr/      # Low-resolution images
├── hr/      # High-resolution images
└── compare/ # Comparison images
```

## Notes

- Images should be in PNG format
- File naming convention: `{category}_{index:04d}.png`
- The dashboard automatically detects available images
- Maximum 50 images are shown in the gallery per session

## Browser Support

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

**Dashboard not loading images?**
- Ensure results are generated in the `results/` directory
- Check that images are in PNG format
- Verify directory permissions

**Port 5000 already in use?**
- Edit `app.py` and change the port number
- Or: `lsof -i :5000` and kill the process

**Metrics showing N/A?**
- Run inference test to generate `results/metrics.json`
- Or update the inference script to create the metrics file

## Future Enhancements

- [ ] Real-time metrics computation
- [ ] Training progress visualization
- [ ] Model performance graphs
- [ ] Batch processing visualization
- [ ] Export results as PDF report
- [ ] Dark mode theme

---

**Project**: Satellite Super-Resolution  
**Model**: CGA (Channel-wise Gated Attention)  
**Scale Factor**: 4x  
**Dashboard Version**: 1.0
