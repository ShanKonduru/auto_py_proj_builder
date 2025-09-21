@echo off
REM =====================================================================
REM Python Framework Generator - Virtual Environment Setup
REM =====================================================================
REM This script creates a Python virtual environment and installs all 
REM required dependencies for the Python Framework Generator project.
REM =====================================================================

echo.
echo ========================================
echo Python Framework Generator - Setup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ and add it to your PATH
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version

REM Check if virtual environment already exists
if exist "venv\" (
    echo.
    echo WARNING: Virtual environment 'venv' already exists
    echo Do you want to recreate it? This will delete the existing environment.
    set /p choice="Continue? (y/N): "
    if /i not "%choice%"=="y" (
        echo Setup cancelled by user
        pause
        exit /b 0
    )
    echo [2/5] Removing existing virtual environment...
    rmdir /s /q venv
)

echo [2/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure you have Python 3.3+ with venv module installed
    pause
    exit /b 1
)

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [4/5] Upgrading pip...
python -m pip install --upgrade pip

echo [5/5] Installing project dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Check requirements.txt file and your internet connection
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Virtual environment created in: %cd%\venv
echo.
echo Next steps:
echo 1. Run 'activate.bat' to activate the environment
echo 2. Run 'run_tests.bat' to run the test suite
echo 3. Run 'run_app.bat' to test the application
echo.
echo You can also manually activate with: venv\Scripts\activate.bat
echo.
pause