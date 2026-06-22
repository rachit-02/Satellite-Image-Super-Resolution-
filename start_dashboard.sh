#!/bin/bash

# Dashboard startup script
echo "🚀 Starting Satellite Super-Resolution Dashboard..."
echo "📊 Dashboard will be available at: http://localhost:5000"
echo ""

cd "$(dirname "$0")"
python3 dashboard/app.py
