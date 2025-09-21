# Batch Files and Shell Scripts Guide

This directory contains batch files for Windows and shell scripts for Unix/Linux to help you work with the Python Framework Generator project across different operating systems.

## Available Scripts

### Windows (.bat files)

#### 1. `create_venv.bat` - Setup Virtual Environment

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

### Unix/Linux (.sh files)

#### 1. `create_venv.sh` - Setup Virtual Environment

**Purpose**: Creates a Python virtual environment and installs all project dependencies on Unix/Linux systems.

**What it does**:

- Checks for Python 3.9+ installation (python3 or python)
- Creates a new virtual environment in `venv/` directory
- Upgrades pip to the latest version
- Installs all dependencies from `requirements.txt`
- Provides platform-specific installation guidance

**Usage**:

```bash
./create_venv.sh
# or
bash create_venv.sh
```

**When to use**: First time setup or when you want to recreate the environment from scratch.

#### 2. `activate.sh` - Activate Environment

**Purpose**: Activates the virtual environment and sets up the development environment on Unix/Linux.

**What it does**:

- Activates the Python virtual environment
- Shows current Python and pip versions
- Sets up PYTHONPATH for development
- Starts a new shell with the environment activated

**Usage**:

```bash
./activate.sh
# or
source activate.sh
```

**When to use**: Every time you want to work on the project.

#### 3. `run_tests.sh` - Test Runner

**Purpose**: Runs the complete test suite with coverage reporting on Unix/Linux systems.

**What it does**:

- Automatically activates virtual environment if needed
- Runs syntax checks on core modules
- Executes unit tests separately
- Executes integration tests separately
- Generates coverage reports (HTML and terminal)
- Attempts to open coverage report in browser (xdg-open/open)

**Usage**:

```bash
./run_tests.sh
```

**When to use**: Before committing changes, during development, or for CI/CD validation.

#### 4. `run_app.sh` - Application Demo

**Purpose**: Interactive demo of the Python Framework Generator CLI functionality on Unix/Linux.

**What it does**:

- Provides an interactive menu system
- Demonstrates various CLI commands
- Allows generation of sample projects
- Shows help and version information
- Supports custom project generation with user input

**Usage**:

```bash
./run_app.sh
```

**When to use**: To test the application, demo functionality, or generate actual projects.

## Quick Start Workflow

### Windows

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

### Unix/Linux/macOS

1. **First time setup**:

   ```bash
   ./create_venv.sh
   ```

2. **Daily development**:

   ```bash
   ./activate.sh
   ```

3. **Run tests**:

   ```bash
   ./run_tests.sh
   ```

4. **Test the application**:

   ```bash
   ./run_app.sh
   ```

**Note**: On Unix/Linux systems, you may need to make scripts executable first:

```bash
chmod +x *.sh
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

**Windows**:
- Install Python 3.9+ from python.org
- Make sure Python is added to your system PATH

**Unix/Linux**:
- Ubuntu/Debian: `sudo apt-get install python3 python3-venv python3-pip`
- CentOS/RHEL: `sudo yum install python3 python3-venv python3-pip`
- macOS: `brew install python3`

### "Virtual environment not found"

**Windows**: Run `create_venv.bat` first to create the environment

**Unix/Linux**: Run `./create_venv.sh` first to create the environment

### "Failed to install dependencies"

- Check your internet connection
- Ensure `requirements.txt` exists and is properly formatted
- Try running `pip install --upgrade pip` manually

### "Permission denied" (Unix/Linux only)

- Make scripts executable: `chmod +x *.sh`
- Ensure you have write permissions in the project directory

### Tests failing

- Ensure virtual environment is activated
- Check if all dependencies are installed
- Review test output for specific error messages

## Advanced Usage

### Manual Commands

**Windows** - After activating the environment with `activate.bat`:

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

**Unix/Linux** - After activating the environment with `./activate.sh`:

```bash
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

You can modify these scripts to suit your specific needs:

- Change default output directories
- Add additional test configurations
- Modify the interactive menu options
- Add custom project templates

**Platform-specific customizations**:

- Windows: Edit `.bat` files with any text editor
- Unix/Linux: Edit `.sh` files and ensure they remain executable (`chmod +x *.sh`)