@echo off
REM =====================================================================
REM Python Framework Generator - Environment Activation
REM =====================================================================
REM This script activates the Python virtual environment for the
REM Python Framework Generator project and provides useful information.
REM =====================================================================

echo.
echo ========================================
echo Python Framework Generator - Activate
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found
    echo Run 'create_venv.bat' first to create the virtual environment
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Try recreating it with 'create_venv.bat'
    pause
    exit /b 1
)

echo.
echo ========================================
echo Environment activated successfully!
echo ========================================
echo.
echo Python version:
python --version
echo.
echo Pip version:
pip --version
echo.
echo Project location: %cd%
echo Virtual environment: %cd%\venv
echo.
echo Available commands:
echo - run_tests.bat    : Run the test suite
echo - run_app.bat      : Run the application demo
echo - deactivate       : Exit virtual environment
echo.
echo You can now use Python and pip commands in this environment.
echo Type 'deactivate' to exit the virtual environment.
echo.

REM Keep the command prompt open with the activated environment
cmd /k "echo Environment is ready for development!"