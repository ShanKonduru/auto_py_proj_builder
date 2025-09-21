#!/bin/bash
# =====================================================================
# Python Framework Generator - Virtual Environment Setup (Unix/Linux)
# =====================================================================
# This script creates a Python virtual environment and installs all 
# required dependencies for the Python Framework Generator project.
# =====================================================================

set -e  # Exit on any error

echo ""
echo "========================================"
echo "Python Framework Generator - Setup"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.9+ and add it to your PATH"
        echo "On Ubuntu/Debian: sudo apt-get install python3 python3-venv python3-pip"
        echo "On CentOS/RHEL: sudo yum install python3 python3-venv python3-pip"
        echo "On macOS: brew install python3"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "[1/5] Checking Python version..."
$PYTHON_CMD --version

# Check Python version is 3.9+
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
MIN_VERSION="3.9"

if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    echo "ERROR: Python $PYTHON_VERSION found, but Python $MIN_VERSION or higher is required"
    exit 1
fi

# Check if virtual environment already exists
if [ -d "venv" ]; then
    echo ""
    echo "WARNING: Virtual environment 'venv' already exists"
    echo "Do you want to recreate it? This will delete the existing environment."
    read -p "Continue? (y/N): " choice
    case "$choice" in 
        y|Y ) 
            echo "[2/5] Removing existing virtual environment..."
            rm -rf venv
            ;;
        * ) 
            echo "Setup cancelled by user"
            exit 0
            ;;
    esac
fi

echo "[2/5] Creating virtual environment..."
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo "Make sure you have Python 3.3+ with venv module installed"
    echo "On Ubuntu/Debian: sudo apt-get install python3-venv"
    echo "On CentOS/RHEL: sudo yum install python3-venv"
    exit 1
fi

echo "[3/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[4/5] Upgrading pip..."
python -m pip install --upgrade pip

echo "[5/5] Installing project dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        echo "Check requirements.txt file and your internet connection"
        exit 1
    fi
else
    echo "WARNING: requirements.txt not found, skipping dependency installation"
fi

echo ""
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "Virtual environment created in: $(pwd)/venv"
echo ""
echo "Next steps:"
echo "1. Run './activate.sh' to activate the environment"
echo "2. Run './run_tests.sh' to run the test suite"
echo "3. Run './run_app.sh' to test the application"
echo ""
echo "You can also manually activate with: source venv/bin/activate"
echo ""
echo "Press Enter to continue..."
read