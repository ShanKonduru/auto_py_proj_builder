# Data Model: Python Framework Generator

## Core Entities

### ProjectTemplate

Represents the complete blueprint for generating a Python project structure.

**Attributes**:
- `name`: string - Project name (validated for Python package compatibility)
- `description`: string - Project description for README and setup files
- `author`: string - Author name for project metadata
- `email`: string - Author email for project metadata
- `python_version`: string - Minimum Python version requirement
- `include_batch_files`: boolean - Whether to generate Windows batch files
- `template_type`: enum - Type of project template (basic, web, cli, library)

**Validation Rules**:
- Project name must be valid Python identifier
- Python version must be >= 3.9
- Email must be valid email format if provided

**State Transitions**:
1. Created → Validated → Generated → Completed

### TemplateFile

Represents individual file templates within a project structure.

**Attributes**:
- `file_path`: string - Relative path where file should be created
- `template_content`: string - Jinja2 template content
- `is_executable`: boolean - Whether file should have execute permissions
- `platform_specific`: enum - Platform compatibility (all, windows, unix)

**Relationships**:
- Multiple TemplateFiles belong to one ProjectTemplate

### ProjectMetadata

Represents user-provided information for project customization.

**Attributes**:
- `project_name`: string - User-specified project name
- `target_directory`: string - Directory where project will be created
- `author_info`: dict - Author name and email
- `custom_markers`: list - Additional pytest markers to include
- `dependencies`: list - Custom dependencies beyond defaults

**Validation Rules**:
- Target directory must be writable
- Project name must not conflict with existing directories
- Dependencies must be valid package names

### ConfigurationProfile

Represents different testing and quality tool configurations.

**Attributes**:
- `pytest_markers`: list - Standard pytest markers to include
- `coverage_settings`: dict - Code coverage configuration options
- `quality_tools`: list - Static analysis tools to configure
- `pre_commit_hooks`: list - Pre-commit hook configurations

**Default Profiles**:
- Basic: Essential testing setup
- Advanced: Full quality toolchain
- Minimal: Lightweight configuration

## Entity Relationships

```
ProjectTemplate (1) ──→ (many) TemplateFile
ProjectTemplate (1) ──→ (1) ConfigurationProfile
ProjectTemplate (1) ──→ (1) ProjectMetadata
```

## File Generation Workflow

1. **Input Validation**: Validate ProjectMetadata against business rules
2. **Template Selection**: Choose TemplateFiles based on ProjectTemplate.template_type
3. **Content Generation**: Process Jinja2 templates with ProjectMetadata variables
4. **File Creation**: Write generated content to target directory structure
5. **Permission Setting**: Apply executable permissions where needed
6. **Validation**: Verify all required files were created successfully