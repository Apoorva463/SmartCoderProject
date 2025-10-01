#!/bin/bash

echo "🚀 Setting up Website Content Search Application"
echo "================================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Node.js and Python are available"

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

echo "✅ Frontend dependencies installed"

# Create and activate virtual environment
echo "📦 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install setuptools first
echo "📦 Upgrading pip and installing build tools..."
pip install --upgrade pip setuptools wheel

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements-simple.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    exit 1
fi

echo "✅ Backend dependencies installed"

# Create directories if they don't exist
mkdir -p backend/services
mkdir -p src/components
mkdir -p public

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. Start the backend: ./start_backend.sh"
echo "2. Start the frontend: npm start"
echo ""
echo "The application will be available at:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo ""
echo "Note: For full semantic search capabilities, install and run Milvus:"
echo "docker run -d --name milvus-standalone -p 19530:19530 -p 9091:9091 milvusdb/milvus:latest"
