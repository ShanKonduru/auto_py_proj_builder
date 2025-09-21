#!/bin/bash
# =====================================================================
# Python Framework Generator - Application Runner (Unix/Linux)
# =====================================================================
# This script demonstrates the Python Framework Generator CLI
# functionality with example commands and interactive options.
# =====================================================================

echo ""
echo "========================================"
echo "Python Framework Generator - Demo"
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
echo "Framework Generator location: $(pwd)"
echo ""

# Main menu function
show_menu() {
    echo "========================================"
    echo "Choose an option:"
    echo "========================================"
    echo ""
    echo "1. Show help and available commands"
    echo "2. Show version information"
    echo "3. List available templates"
    echo "4. Generate a sample project (basic)"
    echo "5. Generate a sample project (CLI)"
    echo "6. Generate a sample project (web API)"
    echo "7. Run custom generate command"
    echo "8. Validate project configuration"
    echo "9. Exit"
    echo ""
}

# Function to handle each menu option
handle_choice() {
    case "$1" in
        1)
            echo ""
            echo "========================================"
            echo "Framework Generator Help"
            echo "========================================"
            echo ""
            python -m src.cli.main --help
            echo ""
            ;;
        2)
            echo ""
            echo "========================================"
            echo "Version Information"
            echo "========================================"
            echo ""
            python -m src.cli.main --version || echo "Version: Development Build"
            echo ""
            ;;
        3)
            echo ""
            echo "========================================"
            echo "Available Templates"
            echo "========================================"
            echo ""
            python -m src.cli.main list-templates 2>/dev/null || echo "Templates: basic, cli, web, api, lib"
            echo ""
            ;;
        4)
            echo ""
            echo "========================================"
            echo "Generating Basic Project"
            echo "========================================"
            echo ""
            mkdir -p demo_output
            python -m src.cli.main generate demo_basic_project --template basic --output-dir demo_output --author "Demo User" --email "demo@example.com"
            echo ""
            if [ -d "demo_output/demo_basic_project" ]; then
                echo "✓ Basic project generated successfully in demo_output/demo_basic_project/"
                ls -la demo_output/demo_basic_project/
            else
                echo "✗ Project generation failed"
            fi
            echo ""
            ;;
        5)
            echo ""
            echo "========================================"
            echo "Generating CLI Project"
            echo "========================================"
            echo ""
            mkdir -p demo_output
            python -m src.cli.main generate demo_cli_project --template cli --output-dir demo_output --author "Demo User" --email "demo@example.com"
            echo ""
            if [ -d "demo_output/demo_cli_project" ]; then
                echo "✓ CLI project generated successfully in demo_output/demo_cli_project/"
                ls -la demo_output/demo_cli_project/
            else
                echo "✗ Project generation failed"
            fi
            echo ""
            ;;
        6)
            echo ""
            echo "========================================"
            echo "Generating Web API Project"
            echo "========================================"
            echo ""
            mkdir -p demo_output
            python -m src.cli.main generate demo_web_project --template web --output-dir demo_output --author "Demo User" --email "demo@example.com"
            echo ""
            if [ -d "demo_output/demo_web_project" ]; then
                echo "✓ Web project generated successfully in demo_output/demo_web_project/"
                ls -la demo_output/demo_web_project/
            else
                echo "✗ Project generation failed"
            fi
            echo ""
            ;;
        7)
            echo ""
            echo "========================================"
            echo "Custom Project Generation"
            echo "========================================"
            echo ""
            read -p "Enter project name: " project_name
            read -p "Enter template type (basic/cli/web/api/lib): " template_type
            read -p "Enter author name: " author_name
            read -p "Enter author email: " author_email
            read -p "Enter output directory (or press Enter for demo_output): " output_dir
            
            if [ -z "$output_dir" ]; then
                output_dir="demo_output"
            fi
            
            mkdir -p "$output_dir"
            
            echo ""
            echo "Generating project with:"
            echo "- Name: $project_name"
            echo "- Template: $template_type"
            echo "- Author: $author_name"
            echo "- Email: $author_email"
            echo "- Output: $output_dir"
            echo ""
            
            python -m src.cli.main generate "$project_name" --template "$template_type" --output-dir "$output_dir" --author "$author_name" --email "$author_email"
            
            echo ""
            if [ -d "$output_dir/$project_name" ]; then
                echo "✓ Project generated successfully in $output_dir/$project_name/"
                ls -la "$output_dir/$project_name/"
            else
                echo "✗ Project generation failed"
            fi
            echo ""
            ;;
        8)
            echo ""
            echo "========================================"
            echo "Project Validation"
            echo "========================================"
            echo ""
            python -m src.cli.main validate 2>/dev/null || echo "Validation command not implemented yet"
            echo ""
            ;;
        9)
            echo ""
            echo "========================================"
            echo "Demo Complete"
            echo "========================================"
            echo ""
            echo "Generated projects are available in the demo_output/ directory"
            echo ""
            echo "To clean up demo files:"
            echo "   rm -rf demo_output"
            echo ""
            echo "Thank you for using Python Framework Generator!"
            echo ""
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            echo ""
            ;;
    esac
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice (1-9): " choice
    handle_choice "$choice"
    echo "Press Enter to continue..."
    read
done