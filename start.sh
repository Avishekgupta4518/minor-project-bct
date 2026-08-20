#!/bin/bash
# start.sh - Quick start script for the Smart Multi-Crop application

echo "=================================="
echo "Smart Multi-Crop System"
echo "Starting Application..."
echo "=================================="
echo ""

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    exit 1
fi

echo "✓ Python found: $(python --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🚀 Starting Flask application..."
echo "📍 Open browser: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Run the app
python app.py
