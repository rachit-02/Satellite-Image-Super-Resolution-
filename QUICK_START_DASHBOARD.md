# 🚀 Quick Start: Dashboard

## Step 1: Start the Dashboard

```bash
cd /home/sushil.ghildiyal/Minor_Satellite_SR_Nimit_Rachit_Dhananjay
./start_dashboard.sh
```

Or:
```bash
cd dashboard
python3 app.py
```

## Step 2: Open in Browser

Once you see:
```
Running on http://0.0.0.0:5000
```

Open your browser and go to:
```
http://localhost:5000
```

## Step 3: Explore Your Results

✅ **Metrics Section** - View PSNR and SSIM scores  
✅ **Statistics** - See image counts and project info  
✅ **Gallery** - Browse LR, SR, HR, and comparison images  
✅ **Navigation** - Use Previous/Next or jump to image #  

## Features

### 📊 Real-time Metrics
- Average PSNR (dB)
- Average SSIM (0-1)
- Total images processed

### 🖼️ Image Gallery
- Side-by-side comparison view
- Low-resolution input
- Super-resolution output
- High-resolution ground truth

### 📱 Responsive Design
- Works on desktop, tablet, mobile
- Beautiful gradient UI
- Professional animations

## API for Developers

Get data via REST API:

```bash
# Get metrics
curl http://localhost:5000/api/metrics

# Get statistics
curl http://localhost:5000/api/statistics

# Get image list
curl http://localhost:5000/api/images

# Get specific image (base64 PNG)
curl http://localhost:5000/api/image/sr/sr_0000.png
```

## Troubleshooting

**Port already in use?**
Check which process is using port 5000 and note its PID, then stop the Flask server.

**No images showing?**
- Run `python3 inference/test.py` first to generate results
- Check `results/` directory exists
- Verify images are in PNG format

**Need more info?**
- See `DASHBOARD_GUIDE.md` for complete documentation
- Check `dashboard/README.md` for detailed API reference

---

Enjoy your professional dashboard! 🎉
