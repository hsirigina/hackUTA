#!/bin/bash
# Quick script to run the BLE monitor with proper environment

echo "🚀 Starting Arduino BLE Monitor..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Run the BLE script
python3 ble.py

# Deactivate when done
deactivate
