#!/bin/bash
# =====================================================================
# Python Framework Generator - Test Runner (Unix/Linux)
# =====================================================================
# This script runs the test suite with proper configuration and 
# generates coverage reports for the Python Framework Generator.
# =====================================================================

set -e  # Exit on any error except where explicitly handled

echo ""
echo "========================================"
echo "Python Framework Generator - Tests"
echo "========================================"
echo ""

# Function to check if we're in a virtual environment
is_venv_active() {
    if [[ "$VIRTUAL_ENV" != "" ]] || [[ "$CONDA_DEFAULT_ENV" != "" ]]; then
        return 0
    else
        return 1
    fi
}

# Check if virtual environment is activated
if ! is_venv_active; then
    echo "WARNING: Virtual environment not detected"
    echo ""
    echo "Checking if venv exists and trying to activate..."
    if [ -d "venv" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to activate virtual environment"
            exit 1
        fi
    else
        echo "ERROR: No virtual environment found"
        echo "Run './create_venv.sh' first to set up the environment"
        exit 1
    fi
fi

echo "Current Python environment:"
python --version
echo ""

# Check if pytest is installed
if ! python -c "import pytest" &> /dev/null; then
    echo "ERROR: pytest not installed"
    echo "Installing pytest..."
    pip install pytest pytest-cov
    if [ $? -ne 0 ]; then
        echo "Failed to install pytest"
        exit 1
    fi
fi

# Initialize result variables
unit_result=0
integration_result=0
coverage_result=0

echo "[1/4] Running syntax and import checks..."
if python -m py_compile src/cli/main.py; then
    echo "✓ Syntax check passed"
else
    echo "✗ Syntax error in main module"
    exit 1
fi

echo ""
echo "[2/4] Running unit tests..."
set +e  # Don't exit on test failures, we want to collect all results
python -m pytest tests/ -v --tb=short -m "not integration and not slow"
unit_result=$?
set -e

echo ""
echo "[3/4] Running integration tests..."
set +e
python -m pytest tests/ -v --tb=short -m "integration and not slow"
integration_result=$?
set -e

echo ""
echo "[4/4] Running all tests with coverage..."
set +e
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing --tb=short
coverage_result=$?
set -e

echo ""
echo "========================================"
echo "Test Results Summary"
echo "========================================"
echo ""

if [ $unit_result -eq 0 ]; then
    echo "✓ Unit tests: PASSED"
else
    echo "✗ Unit tests: FAILED"
fi

if [ $integration_result -eq 0 ]; then
    echo "✓ Integration tests: PASSED"
else
    echo "✗ Integration tests: FAILED"
fi

if [ $coverage_result -eq 0 ]; then
    echo "✓ Coverage report: Generated"
else
    echo "✗ Coverage report: FAILED"
fi

echo ""
if [ -f "htmlcov/index.html" ]; then
    echo "Coverage report available at: htmlcov/index.html"
    echo ""
    read -p "Open coverage report in browser? (y/N): " choice
    case "$choice" in 
        y|Y ) 
            # Try to open in browser (works on most Linux desktops and macOS)
            if command -v xdg-open &> /dev/null; then
                xdg-open htmlcov/index.html
            elif command -v open &> /dev/null; then
                open htmlcov/index.html
            else
                echo "Could not open browser automatically. Please open htmlcov/index.html manually."
            fi
            ;;
        * ) 
            ;;
    esac
fi

echo ""
echo "Available test markers:"
echo "- pytest tests/ -m unit          : Run only unit tests"
echo "- pytest tests/ -m integration   : Run only integration tests"
echo "- pytest tests/ -m smoke         : Run smoke tests"
echo "- pytest tests/ -m slow          : Run slow tests"
echo ""

# Exit with error code if any tests failed
if [ $unit_result -ne 0 ] || [ $integration_result -ne 0 ] || [ $coverage_result -ne 0 ]; then
    echo "Some tests failed. Check the output above for details."
    exit 1
fi

echo "All tests completed successfully!"
echo "Press Enter to continue..."
read