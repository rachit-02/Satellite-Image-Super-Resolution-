# 🔧 Fixing Metrics Display Issue

## Problem
The dashboard shows metrics as **0.00** (PSNR) and **0.0000** (SSIM) instead of actual values.

## Root Cause
The `results/metrics.json` file doesn't exist yet. It's created when you run the inference script (`inference/test.py`), which calculates PSNR and SSIM metrics.

## Solution

### Option 1: Generate Real Metrics (Recommended)

Run the inference script to generate actual metrics:

```bash
python3 inference/test.py
```

This will:
1. Run super-resolution inference on test images
2. Calculate PSNR and SSIM scores
3. Generate result images in `results/` directory
4. Create `results/metrics.json` with the metrics
5. Metrics will automatically update in the dashboard (auto-refresh)

### Option 2: Create Sample Metrics File (For Testing)

If you want to see the dashboard working with metrics immediately:

```bash
chmod +x generate_metrics.sh
./generate_metrics.sh
```

This script will:
- Check if metrics.json exists
- Show instructions if it doesn't
- Optionally create a sample metrics.json file

### Option 3: Manual Metrics File

Create `results/metrics.json` manually:

```bash
mkdir -p results
cat > results/metrics.json << 'EOF'
{
    "psnr": 32.45,
    "ssim": 0.8234,
    "total_images": 50,
    "last_updated": "2026-05-04 14:35:00"
}
EOF
```

Then refresh the dashboard - metrics will update immediately!

## How It Works

1. **Metrics Generation**: `inference/test.py` calculates PSNR and SSIM
2. **File Creation**: Metrics saved to `results/metrics.json`
3. **Dashboard Loading**: Dashboard API reads this file
4. **Display Update**: Metrics show in the dashboard UI
5. **Auto-Refresh**: Updates every 30 seconds

## Metrics File Format

```json
{
    "psnr": 32.45,           // Peak Signal-to-Noise Ratio (dB)
    "ssim": 0.8234,          // Structural Similarity Index (0-1)
    "total_images": 50,      // Number of images processed
    "last_updated": "timestamp"  // When metrics were generated
}
```

## What to Expect

✅ **After Running Inference**:
- PSNR shows something like **30-40** dB
- SSIM shows something like **0.7-0.9**
- Last Updated shows actual timestamp

❌ **Before Running Inference**:
- PSNR shows **N/A**
- SSIM shows **N/A**
- Check browser console for guidance

## Troubleshooting

### "Still showing 0.00 after running inference?"

1. Verify inference completed successfully:
   ```bash
   tail -20 inference.log  # Check output
   ```

2. Check if metrics.json was created:
   ```bash
   cat results/metrics.json
   ```

3. Refresh the dashboard in browser (Ctrl+R or Cmd+R)

4. Check browser console (F12) for any errors

### "Getting permission denied?"

Make sure the results directory is writable:
```bash
chmod 755 results/
chmod 644 results/metrics.json
```

### "Dashboard still showing old values?"

The dashboard caches values. Try:
1. Hard refresh: **Ctrl+Shift+R** (Windows/Linux) or **Cmd+Shift+R** (Mac)
2. Or clear browser cache
3. Wait 30 seconds for auto-refresh

## Quick Workflow

```bash
# 1. Generate real metrics
python3 inference/test.py

# 2. Wait for completion (check for "metrics saved" message)

# 3. Dashboard auto-updates! Or manually refresh

# 4. See real PSNR/SSIM values in dashboard
```

## Testing the API

You can test if metrics are loading correctly:

```bash
# Check if metrics file exists
cat results/metrics.json

# Test API endpoint directly
curl http://localhost:5000/api/metrics

# Should return something like:
# {"psnr": 32.45, "ssim": 0.8234, "total_images": 50, ...}
```

## Next Steps

1. **Run Inference**: `python3 inference/test.py`
2. **Wait for Completion**: Watch for "Metrics saved" message
3. **Refresh Dashboard**: Metrics will update automatically
4. **Verify**: PSNR and SSIM should show real values

---

**Still having issues?** Check the browser console (F12) for error messages, or verify that `results/metrics.json` exists and contains valid JSON.
