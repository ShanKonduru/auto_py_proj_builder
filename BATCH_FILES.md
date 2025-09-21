# Batch Files Guide

This directory contains several batch files to help you work with the Python Framework Generator project on Windows.

## Available Batch Files

### 1. `create_venv.bat` - Setup Virtual Environment

**Purpose**: Creates a Python virtual environment and installs all project dependencies.

**What it does**:

- Checks for Python installation
- Creates a new virtual environment in `venv/` directory
- Upgrades pip to the latest version
- Installs all dependencies from `requirements.txt`
- Provides setup completion status

**Usage**:

```cmd
create_venv.bat
```

**When to use**: First time setup or when you want to recreate the environment from scratch.

### 2. `activate.bat` - Activate Environment

**Purpose**: Activates the virtual environment and opens a command prompt ready for development.

**What it does**:

- Activates the Python virtual environment
- Shows current Python and pip versions
- Displays helpful information about available commands
- Keeps the command prompt open with the activated environment

**Usage**:

```cmd
activate.bat
```

**When to use**: Every time you want to work on the project.

### 3. `run_tests.bat` - Test Runner

**Purpose**: Runs the complete test suite with coverage reporting.

**What it does**:

- Automatically activates virtual environment if needed
- Runs syntax checks on core modules
- Executes unit tests separately
- Executes integration tests separately
- Generates coverage reports (HTML and terminal)
- Provides option to open coverage report in browser

**Usage**:

```cmd
run_tests.bat
```

**When to use**: Before committing changes, during development, or for CI/CD validation.

### 4. `run_app.bat` - Application Demo

**Purpose**: Interactive demo of the Python Framework Generator CLI functionality.

**What it does**:

- Provides an interactive menu system
- Demonstrates various CLI commands
- Allows generation of sample projects
- Shows help and version information
- Supports custom project generation with user input

**Usage**:

```cmd
run_app.bat
```

**When to use**: To test the application, demo functionality, or generate actual projects.

## Quick Start Workflow

1. **First time setup**:

   ```cmd
   create_venv.bat
   ```

2. **Daily development**:

   ```cmd
   activate.bat
   ```

3. **Run tests**:

   ```cmd
   run_tests.bat
   ```

4. **Test the application**:

   ```cmd
   run_app.bat
   ```

## Features

### Smart Environment Detection

All batch files automatically detect if a virtual environment is active and attempt to activate one if needed.

### Error Handling

Comprehensive error checking with helpful error messages and guidance for resolution.

### Interactive Menus

The application runner provides an easy-to-use menu system for testing different features.

### Coverage Reports

Test runner generates both HTML and terminal coverage reports, with option to open in browser.

### Demo Project Generation

The application runner can generate sample projects in a `demo_output/` directory for testing.

## Troubleshooting

### "Python is not installed or not in PATH"

- Install Python 3.9+ from python.org
- Make sure Python is added to your system PATH

### "Virtual environment not found"

- Run `create_venv.bat` first to create the environment

### "Failed to install dependencies"

- Check your internet connection
- Ensure `requirements.txt` exists and is properly formatted
- Try running `pip install --upgrade pip` manually

### Tests failing

- Ensure virtual environment is activated
- Check if all dependencies are installed
- Review test output for specific error messages

## Advanced Usage

### Manual Commands

After activating the environment with `activate.bat`, you can run manual commands:

```cmd
# Run specific test categories
python -m pytest tests/ -m unit
python -m pytest tests/ -m integration
python -m pytest tests/ -m smoke

# Generate projects manually
python -m src.cli.main generate my_project --template basic --author "Your Name"

# Show help
python -m src.cli.main --help
```

### Customization

You can modify these batch files to suit your specific needs:

- Change default output directories
- Add additional test configurations
- Modify the interactive menu options
- Add custom project templates