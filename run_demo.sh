#!/bin/bash
# Run the Python MVP market-making demo

set -e  # Exit on error

echo "=== Low-Latency Market-Making Demo ==="
echo "Using sample data from data/sample_ticks.csv"
echo "----------------------------------------"

# Activate virtualenv if you have one
# source venv/bin/activate

# Run the main Python script
python3 src_python/main.py

echo "----------------------------------------"
echo "Demo complete."

