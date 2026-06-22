#!/bin/bash

# Script to generate sample metrics or show how to get real metrics

METRICS_FILE="results/metrics.json"

echo "========================================"
echo "📊 Metrics File Generator"
echo "========================================"
echo ""

if [ -f "$METRICS_FILE" ]; then
    echo "✅ Metrics file already exists:"
    cat "$METRICS_FILE"
    echo ""
else
    echo "❌ No metrics.json found"
    echo ""
    echo "To generate real metrics, run:"
    echo "  python3 inference/test.py"
    echo ""
    echo "This will:"
    echo "  1. Run inference on test images"
    echo "  2. Calculate PSNR and SSIM metrics"
    echo "  3. Generate results in results/ directory"
    echo "  4. Save metrics to results/metrics.json"
    echo ""
    echo "Then refresh the dashboard to see the metrics!"
    echo ""
    
    # Optionally create a placeholder metrics file for demo
    read -p "Create sample metrics file for demonstration? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mkdir -p results
        cat > "$METRICS_FILE" << 'EOF'
{
    "psnr": 32.45,
    "ssim": 0.8234,
    "total_images": 50,
    "last_updated": "2026-05-04 14:30:00"
}
EOF
        echo "✅ Sample metrics.json created!"
        echo "   (Replace with real metrics by running: python3 inference/test.py)"
        cat "$METRICS_FILE"
    fi
fi
