#!/bin/bash
# Run the Python MVP market-making demo

set -e  # Exit on error

echo "=== Low-Latency Market-Making Demo ==="
echo "Using sample data from data/sample_ticks.csv"
echo "----------------------------------------"

# Activate virtualenv if you have one
# source venv/bin/activate

# Run the main Python script
echo "[RUN]  Starting market-making engine..."
python3 src_python/main2.py & ENGINE_PID=$!

sleep 1

echo "[RUN]  Starting UI dashboard..."
python3 src_python/ui_client.py

echo "[RUN]  Stopping engine ..."
kill $ENGINE_PID

echo "----------------------------------------"
echo "Demo complete."

