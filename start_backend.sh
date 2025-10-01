#!/bin/bash

# Start the Python backend server
echo "Starting Website Content Search Backend..."
echo "Activating virtual environment..."

# Activate virtual environment
source venv/bin/activate

echo "Starting FastAPI server..."
echo ""

cd backend
python main.py
