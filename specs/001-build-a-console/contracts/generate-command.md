# CLI Contract: Generate Command

## Command Signature
```bash
python-framework-gen generate [PROJECT_NAME] [OPTIONS]
```

## Parameters

### Required
- `PROJECT_NAME`: string
  - Description: Name of the Python project to generate
  - Validation: Must be valid Python identifier
  - Example: "my_awesome_project"

### Options
- `--author`: string
  - Description: Author name for project metadata
  - Default: Current system user
  - Example: "John Doe"

- `--email`: string
  - Description: Author email for project metadata
  - Validation: Valid email format
  - Example: "john@example.com"

- `--template`: choice
  - Description: Project template type
  - Choices: basic, web, cli, library
  - Default: basic
  - Example: cli

- `--python-version`: string
  - Description: Minimum Python version requirement
  - Validation: >= 3.9
  - Default: 3.9
  - Example: "3.11"

- `--no-batch-files`: flag
  - Description: Skip Windows batch file generation
  - Default: false (batch files included)

- `--output-dir`: string
  - Description: Target directory for project generation
  - Default: current directory
  - Example: "/path/to/projects"

## Success Response
```
✓ Project 'my_awesome_project' generated successfully!
✓ Created 15 files in /path/to/my_awesome_project/
✓ Run 'cd my_awesome_project && python -m venv .venv' to get started
```

## Error Responses

### Invalid Project Name
```
✗ Error: Project name 'my-project' is invalid
  Project names must be valid Python identifiers (use underscores instead of hyphens)
```

### Directory Already Exists
```
✗ Error: Directory 'my_awesome_project' already exists
  Use --force to overwrite or choose a different name
```

### Permission Denied
```
✗ Error: Permission denied writing to '/path/to/target'
  Check directory permissions and try again
```

### Invalid Python Version
```
✗ Error: Python version '2.7' is not supported
  Minimum required version is 3.9
```

## Exit Codes
- 0: Success
- 1: Invalid arguments
- 2: File system error
- 3: Permission error