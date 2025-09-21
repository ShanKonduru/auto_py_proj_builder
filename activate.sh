#!/bin/bash
# =====================================================================
# Python Framework Generator - Environment Activation (Unix/Linux)
# =====================================================================
# This script activates the Python virtual environment for the
# Python Framework Generator project and provides useful information.
# =====================================================================

echo ""
echo "========================================"
echo "Python Framework Generator - Activate"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found"
    echo "Run './create_venv.sh' first to create the virtual environment"
    echo ""
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    echo "Try recreating it with './create_venv.sh'"
    exit 1
fi

echo ""
echo "========================================"
echo "Environment activated successfully!"
echo "========================================"
echo ""
echo "Python version:"
python --version
echo ""
echo "Pip version:"
pip --version
echo ""
echo "Project location: $(pwd)"
echo "Virtual environment: $(pwd)/venv"
echo ""
echo "Available commands:"
echo "- ./run_tests.sh    : Run the test suite"
echo "- ./run_app.sh      : Run the application demo"
echo "- deactivate        : Exit virtual environment"
echo ""
echo "You can now use Python and pip commands in this environment."
echo "Type 'deactivate' to exit the virtual environment."
echo ""

# Export environment variables for convenience
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

echo "PYTHONPATH updated to include src/ directory"
echo "Environment is ready for development!"
echo ""

# Start a new shell with the environment activated
# This keeps the activation persistent
exec $SHELL