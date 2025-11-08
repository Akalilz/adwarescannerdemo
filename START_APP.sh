#!/bin/bash

# Android Adware Scanner - Startup Script for Mac/Linux

clear
echo "========================================"
echo "  Android Adware Scanner - Web App"
echo "========================================"
echo ""
echo "Starting local web server..."
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Python 3 found! Checking dependencies..."
echo ""

# Check if Flask is installed
python3 -c "import flask" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing required dependencies..."
    echo "This may take a few minutes..."
    echo ""
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to install dependencies!"
        echo "Please run manually: pip3 install -r requirements.txt"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo ""
    echo "Dependencies installed successfully!"
    echo ""
fi

echo "========================================"
echo "  Starting Flask Server"
echo "========================================"
echo ""
echo "The app will open in your browser at:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Try to open browser automatically
sleep 2
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000 &> /dev/null &
elif command -v open &> /dev/null; then
    open http://localhost:5000 &> /dev/null &
fi

# Start Flask app
python3 app.py

# If app exits
echo ""
echo "Server stopped."
read -p "Press Enter to exit..."
