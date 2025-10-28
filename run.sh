#!/bin/bash

# Start script for Stock & Crypto News Sentiment Analysis Platform

echo "=================================="
echo "News Sentiment Analysis Platform"
echo "=================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Start backend
echo "Starting Flask backend..."
python -m backend.app &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

echo ""
echo "=================================="
echo "Backend started on http://localhost:5000"
echo "Backend PID: $BACKEND_PID"
echo "=================================="
echo ""
echo "To start the frontend:"
echo "  cd frontend"
echo "  npm install"
echo "  npm start"
echo ""
echo "To stop the backend:"
echo "  kill $BACKEND_PID"
echo "=================================="

# Keep script running
wait $BACKEND_PID
