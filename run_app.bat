@echo off
REM =====================================================================
REM Python Framework Generator - Application Runner
REM =====================================================================
REM This script demonstrates the Python Framework Generator CLI
REM functionality with example commands and interactive options.
REM =====================================================================

echo.
echo ========================================
echo Python Framework Generator - Demo
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
echo Framework Generator location: %cd%
echo.

:MENU
echo ========================================
echo Choose an option:
echo ========================================
echo.
echo 1. Show help and available commands
echo 2. Show version information
echo 3. List available templates
echo 4. Generate a sample project (basic)
echo 5. Generate a sample project (CLI)
echo 6. Generate a sample project (web API)
echo 7. Run custom generate command
echo 8. Validate project configuration
echo 9. Exit
echo.
set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto HELP
if "%choice%"=="2" goto VERSION
if "%choice%"=="3" goto LIST_TEMPLATES
if "%choice%"=="4" goto GENERATE_BASIC
if "%choice%"=="5" goto GENERATE_CLI
if "%choice%"=="6" goto GENERATE_WEB
if "%choice%"=="7" goto CUSTOM_GENERATE
if "%choice%"=="8" goto VALIDATE
if "%choice%"=="9" goto EXIT
echo Invalid choice. Please try again.
echo.
goto MENU

:HELP
echo.
echo ========================================
echo Framework Generator Help
echo ========================================
echo.
python -m src.cli.main --help
echo.
pause
goto MENU

:VERSION
echo.
echo ========================================
echo Version Information
echo ========================================
echo.
python -m src.cli.main --version
echo.
pause
goto MENU

:LIST_TEMPLATES
echo.
echo ========================================
echo Available Templates
echo ========================================
echo.
python -m src.cli.main list-templates
if errorlevel 1 (
    echo Templates: basic, cli, web, api, lib
)
echo.
pause
goto MENU

:GENERATE_BASIC
echo.
echo ========================================
echo Generating Basic Project
echo ========================================
echo.
if not exist "demo_output\" mkdir demo_output
python -m src.cli.main generate demo_basic_project --template basic --output-dir demo_output --author "Demo User" --email "demo@example.com"
echo.
if exist "demo_output\demo_basic_project\" (
    echo ✓ Basic project generated successfully in demo_output\demo_basic_project\
    dir demo_output\demo_basic_project\
) else (
    echo ✗ Project generation failed
)
echo.
pause
goto MENU

:GENERATE_CLI
echo.
echo ========================================
echo Generating CLI Project
echo ========================================
echo.
if not exist "demo_output\" mkdir demo_output
python -m src.cli.main generate demo_cli_project --template cli --output-dir demo_output --author "Demo User" --email "demo@example.com"
echo.
if exist "demo_output\demo_cli_project\" (
    echo ✓ CLI project generated successfully in demo_output\demo_cli_project\
    dir demo_output\demo_cli_project\
) else (
    echo ✗ Project generation failed
)
echo.
pause
goto MENU

:GENERATE_WEB
echo.
echo ========================================
echo Generating Web API Project
echo ========================================
echo.
if not exist "demo_output\" mkdir demo_output
python -m src.cli.main generate demo_web_project --template web --output-dir demo_output --author "Demo User" --email "demo@example.com"
echo.
if exist "demo_output\demo_web_project\" (
    echo ✓ Web project generated successfully in demo_output\demo_web_project\
    dir demo_output\demo_web_project\
) else (
    echo ✗ Project generation failed
)
echo.
pause
goto MENU

:CUSTOM_GENERATE
echo.
echo ========================================
echo Custom Project Generation
echo ========================================
echo.
set /p project_name="Enter project name: "
set /p template_type="Enter template type (basic/cli/web/api/lib): "
set /p author_name="Enter author name: "
set /p author_email="Enter author email: "
set /p output_dir="Enter output directory (or press Enter for demo_output): "

if "%output_dir%"=="" set output_dir=demo_output
if not exist "%output_dir%\" mkdir "%output_dir%"

echo.
echo Generating project with:
echo - Name: %project_name%
echo - Template: %template_type%
echo - Author: %author_name%
echo - Email: %author_email%
echo - Output: %output_dir%
echo.

python -m src.cli.main generate "%project_name%" --template "%template_type%" --output-dir "%output_dir%" --author "%author_name%" --email "%author_email%"

echo.
if exist "%output_dir%\%project_name%\" (
    echo ✓ Project generated successfully in %output_dir%\%project_name%\
    dir "%output_dir%\%project_name%\"
) else (
    echo ✗ Project generation failed
)
echo.
pause
goto MENU

:VALIDATE
echo.
echo ========================================
echo Project Validation
echo ========================================
echo.
python -m src.cli.main validate
if errorlevel 1 (
    echo Validation command not implemented yet
)
echo.
pause
goto MENU

:EXIT
echo.
echo ========================================
echo Demo Complete
echo ========================================
echo.
echo Generated projects are available in the demo_output\ directory
echo.
echo To clean up demo files:
echo   rmdir /s /q demo_output
echo.
echo Thank you for using Python Framework Generator!
echo.
pause
exit /b 0