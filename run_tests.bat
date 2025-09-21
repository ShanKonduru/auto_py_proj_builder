@echo off
REM =====================================================================
REM Python Framework Generator - Test Runner
REM =====================================================================
REM This script runs the test suite with proper configuration and 
REM generates coverage reports for the Python Framework Generator.
REM =====================================================================

echo.
echo ========================================
echo Python Framework Generator - Tests
echo ========================================
echo.

REM Check if virtual environment is activated
python -c "import sys; exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Virtual environment not detected
    echo.
    echo Checking if venv exists and trying to activate...
    if exist "venv\" (
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
    ) else (
        echo ERROR: No virtual environment found
        echo Run 'create_venv.bat' first to set up the environment
        pause
        exit /b 1
    )
)

echo Current Python environment:
python --version
echo.

REM Check if pytest is installed
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo ERROR: pytest not installed
    echo Installing pytest...
    pip install pytest pytest-cov
    if errorlevel 1 (
        echo Failed to install pytest
        pause
        exit /b 1
    )
)

echo [1/4] Running syntax and import checks...
python -m py_compile src\cli\main.py
if errorlevel 1 (
    echo ERROR: Syntax error in main module
    pause
    exit /b 1
)

echo [2/4] Running unit tests...
python -m pytest tests\ -v --tb=short -m "not integration and not slow"
set unit_result=%errorlevel%

echo.
echo [3/4] Running integration tests...
python -m pytest tests\ -v --tb=short -m "integration and not slow"
set integration_result=%errorlevel%

echo.
echo [4/4] Running all tests with coverage...
python -m pytest tests\ --cov=src --cov-report=html --cov-report=term-missing --tb=short
set coverage_result=%errorlevel%

echo.
echo ========================================
echo Test Results Summary
echo ========================================
echo.

if %unit_result%==0 (
    echo ✓ Unit tests: PASSED
) else (
    echo ✗ Unit tests: FAILED
)

if %integration_result%==0 (
    echo ✓ Integration tests: PASSED
) else (
    echo ✗ Integration tests: FAILED
)

if %coverage_result%==0 (
    echo ✓ Coverage report: Generated
) else (
    echo ✗ Coverage report: FAILED
)

echo.
if exist "htmlcov\index.html" (
    echo Coverage report available at: htmlcov\index.html
    echo.
    set /p choice="Open coverage report in browser? (y/N): "
    if /i "%choice%"=="y" (
        start htmlcov\index.html
    )
)

echo.
echo Available test markers:
echo - pytest tests\ -m unit          : Run only unit tests
echo - pytest tests\ -m integration   : Run only integration tests
echo - pytest tests\ -m smoke         : Run smoke tests
echo - pytest tests\ -m slow          : Run slow tests
echo.
pause