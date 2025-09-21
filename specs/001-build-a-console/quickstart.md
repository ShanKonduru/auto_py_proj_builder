# Quickstart: Python Framework Generator

## Installation Test Scenario

**Objective**: Verify the framework generator can be installed and basic functionality works.

**Steps**:
1. Install the python-framework-gen package
2. Verify the command is available in PATH
3. Run help command to confirm installation
4. Generate a simple test project
5. Verify generated project structure

**Expected Results**:
- Command `python-framework-gen --help` displays usage information
- Test project is created with all expected files
- Generated project passes basic validation checks

## Basic Project Generation Scenario

**Objective**: Generate a basic Python project and verify it's functional.

**Given**: Fresh installation of python-framework-gen  
**When**: User runs `python-framework-gen generate test_project --author "Test User" --email "test@example.com"`  
**Then**: 
- Project directory `test_project/` is created
- Required files are present: `main.py`, `requirements.txt`, `pytest.ini`, `README.md`
- Tests directory contains sample test files with markers
- Windows batch files are generated (if on Windows)
- Generated README contains project information

**Verification Commands**:
```bash
cd test_project
python -m pytest --collect-only  # Should discover test files
pytest --markers              # Should list custom markers
python main.py               # Should run without errors
```

## Advanced Project Generation Scenario

**Objective**: Generate a CLI-type project with custom settings.

**Given**: Framework generator is installed  
**When**: User runs `python-framework-gen generate my_cli_tool --template cli --python-version 3.11 --no-batch-files`  
**Then**: 
- Project structure includes CLI-specific templates
- Python version requirement is set to 3.11
- No Windows batch files are generated
- CLI framework dependencies are included in requirements.txt

## Error Handling Scenarios

### Invalid Project Name Test
**Given**: Framework generator is ready  
**When**: User runs `python-framework-gen generate "my-invalid-name"`  
**Then**: Command fails with clear error message about Python identifier requirements

### Existing Directory Test
**Given**: Directory `existing_project/` already exists  
**When**: User runs `python-framework-gen generate existing_project`  
**Then**: Command fails with error about existing directory

### Permission Error Test
**Given**: Target directory is read-only  
**When**: User attempts to generate project in read-only location  
**Then**: Command fails with permission error and helpful message

## Integration Test Scenarios

### Full Development Workflow
**Objective**: Verify generated project supports complete development lifecycle.

**Steps**:
1. Generate new project with all features
2. Create virtual environment using generated scripts
3. Install dependencies using generated requirements
4. Run initial tests (should pass)
5. Add new test with custom marker
6. Run specific marker tests
7. Generate coverage report
8. Verify all quality tools work

**Acceptance Criteria**:
- All batch files execute successfully
- Tests run and pass with coverage reporting
- Custom markers work correctly
- Development workflow is smooth and error-free

### Multi-Template Validation
**Objective**: Ensure all template types generate functional projects.

**Steps**:
1. Generate project with `--template basic`
2. Generate project with `--template web`
3. Generate project with `--template cli`
4. Generate project with `--template library`
5. Verify each has appropriate structure and dependencies

**Expected Results**:
- Each template creates project-type-specific structure
- Dependencies match template requirements
- Sample code is appropriate for template type
- All projects pass basic validation tests