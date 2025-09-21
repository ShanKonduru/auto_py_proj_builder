"""
TemplateLoader service for Python Framework Generator.
Handles loading and managing project templates.
"""
import os
from pathlib import Path
from typing import Dict, List, Optional

from models.template_file import TemplateFile, PlatformCompatibility
from models.project_template import TemplateType


class TemplateLoader:
    """
    Service for loading and managing project templates.
    
    Handles discovery and loading of template files from the templates directory.
    """
    
    def __init__(self, templates_directory: Optional[str] = None):
        """
        Initialize template loader.
        
        Args:
            templates_directory: Directory containing template files
        """
        if templates_directory is None:
            # Default to templates directory in package
            current_dir = Path(__file__).parent.parent
            templates_directory = current_dir / "templates"
        
        self.templates_directory = Path(templates_directory)
        self._template_cache: Dict[TemplateType, List[TemplateFile]] = {}
    
    def load_templates_for_type(self, template_type: TemplateType) -> List[TemplateFile]:
        """
        Load all template files for a specific template type.
        
        Args:
            template_type: Type of templates to load
            
        Returns:
            List[TemplateFile]: List of template files
        """
        # Check cache first
        if template_type in self._template_cache:
            return self._template_cache[template_type]
        
        template_files = []
        template_dir = self.templates_directory / template_type.value
        
        if not template_dir.exists():
            # Create default templates if directory doesn't exist
            template_files = self._create_default_templates(template_type)
        else:
            # Load templates from directory
            template_files = self._load_templates_from_directory(template_dir)
        
        # Cache the loaded templates
        self._template_cache[template_type] = template_files
        return template_files
    
    def _load_templates_from_directory(self, template_dir: Path) -> List[TemplateFile]:
        """
        Load template files from a directory.
        
        Args:
            template_dir: Directory containing template files
            
        Returns:
            List[TemplateFile]: List of template files
        """
        template_files = []
        
        # Walk through all files in template directory
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(template_dir)
                
                # Read template content
                try:
                    content = file_path.read_text(encoding='utf-8')
                except (UnicodeDecodeError, FileNotFoundError):
                    continue
                
                # Determine platform compatibility
                platform = self._determine_platform_compatibility(str(relative_path))
                
                # Determine if executable
                is_executable = self._is_executable_file(str(relative_path))
                
                template_file = TemplateFile(
                    file_path=str(relative_path),
                    template_content=content,
                    is_executable=is_executable,
                    platform_specific=platform
                )
                
                template_files.append(template_file)
        
        return template_files
    
    def _create_default_templates(self, template_type: TemplateType) -> List[TemplateFile]:
        """
        Create default template files for a template type.
        
        Args:
            template_type: Type of template to create defaults for
            
        Returns:
            List[TemplateFile]: List of default template files
        """
        if template_type == TemplateType.BASIC:
            return self._create_basic_templates()
        elif template_type == TemplateType.CLI:
            return self._create_cli_templates()
        elif template_type == TemplateType.WEB:
            return self._create_web_templates()
        elif template_type == TemplateType.LIBRARY:
            return self._create_library_templates()
        else:
            return self._create_basic_templates()
    
    def _create_basic_templates(self) -> List[TemplateFile]:
        """Create default basic project templates."""
        templates = []
        
        # Main Python file
        main_py_content = '''"""
{{ project_description }}

Author: {{ author_name }}
"""


def main():
    """Main entry point for {{ project_name }}."""
    print("Hello from {{ project_name }}!")


if __name__ == "__main__":
    main()
'''
        templates.append(TemplateFile(
            file_path="main.py",
            template_content=main_py_content
        ))
        
        # Requirements.txt
        requirements_content = '''# Core dependencies for {{ project_name }}
click>=8.1.0
jinja2>=3.1.0

# Development dependencies
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
ruff>=0.1.0
black>=23.0.0
'''
        templates.append(TemplateFile(
            file_path="requirements.txt",
            template_content=requirements_content
        ))
        
        # README.md
        readme_content = '''# {{ project_name }}

{{ project_description }}

## Author

{{ author_name }}{% if author_email %} ({{ author_email }}){% endif %}

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Testing

```bash
pytest
```

## Development

This project was generated using the Python Framework Generator.
'''
        templates.append(TemplateFile(
            file_path="README.md",
            template_content=readme_content
        ))
        
        # Sample test
        test_content = '''"""
Tests for {{ project_name }}.
"""
import pytest


def test_example():
    """Example test function."""
    assert True


@pytest.mark.unit
def test_main_exists():
    """Test that main function exists."""
    from main import main
    assert callable(main)
'''
        templates.append(TemplateFile(
            file_path="tests/test_main.py",
            template_content=test_content
        ))
        
        # Windows batch files
        if "{{ include_batch_files }}" != "false":
            run_bat_content = '''@echo off
echo Running {{ project_name }}...
python main.py
pause
'''
            templates.append(TemplateFile(
                file_path="run.bat",
                template_content=run_bat_content,
                platform_specific=PlatformCompatibility.WINDOWS
            ))
            
            test_bat_content = '''@echo off
echo Running tests for {{ project_name }}...
python -m pytest
pause
'''
            templates.append(TemplateFile(
                file_path="test.bat",
                template_content=test_bat_content,
                platform_specific=PlatformCompatibility.WINDOWS
            ))
        
        return templates
    
    def _create_cli_templates(self) -> List[TemplateFile]:
        """Create CLI-specific templates."""
        templates = self._create_basic_templates()
        
        # CLI-specific main.py
        cli_main_content = '''"""
{{ project_description }}

Command-line interface for {{ project_name }}.

Author: {{ author_name }}
"""
import click


@click.group()
@click.version_option()
def cli():
    """{{ project_description }}"""
    pass


@cli.command()
@click.argument('name', default='World')
def hello(name):
    """Say hello to someone."""
    click.echo(f'Hello {name}!')


@cli.command()
def version():
    """Show version information."""
    click.echo('{{ project_name }} version 0.1.0')


if __name__ == "__main__":
    cli()
'''
        # Replace main.py with CLI version
        for i, template in enumerate(templates):
            if template.file_path == "main.py":
                templates[i] = TemplateFile(
                    file_path="main.py",
                    template_content=cli_main_content
                )
                break
        
        # Add CLI test
        cli_test_content = '''"""
Tests for {{ project_name }} CLI.
"""
import pytest
from click.testing import CliRunner
from main import cli


@pytest.mark.integration
def test_cli_hello():
    """Test hello command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['hello'])
    assert result.exit_code == 0
    assert 'Hello World!' in result.output


@pytest.mark.integration
def test_cli_hello_with_name():
    """Test hello command with custom name."""
    runner = CliRunner()
    result = runner.invoke(cli, ['hello', 'Python'])
    assert result.exit_code == 0
    assert 'Hello Python!' in result.output


@pytest.mark.integration
def test_cli_version():
    """Test version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['version'])
    assert result.exit_code == 0
    assert '{{ project_name }}' in result.output
'''
        templates.append(TemplateFile(
            file_path="tests/test_cli.py",
            template_content=cli_test_content
        ))
        
        return templates
    
    def _create_web_templates(self) -> List[TemplateFile]:
        """Create web application templates."""
        # For now, return basic templates
        # Could be extended with Flask/FastAPI templates
        return self._create_basic_templates()
    
    def _create_library_templates(self) -> List[TemplateFile]:
        """Create library-specific templates."""
        # For now, return basic templates
        # Could be extended with package-specific structure
        return self._create_basic_templates()
    
    def _determine_platform_compatibility(self, file_path: str) -> PlatformCompatibility:
        """
        Determine platform compatibility based on file path.
        
        Args:
            file_path: File path to analyze
            
        Returns:
            PlatformCompatibility: Platform compatibility
        """
        if file_path.endswith('.bat') or file_path.endswith('.cmd'):
            return PlatformCompatibility.WINDOWS
        elif file_path.endswith('.sh'):
            return PlatformCompatibility.UNIX
        else:
            return PlatformCompatibility.ALL
    
    def _is_executable_file(self, file_path: str) -> bool:
        """
        Check if file should be executable.
        
        Args:
            file_path: File path to check
            
        Returns:
            bool: True if file should be executable
        """
        executable_extensions = {'.sh', '.bat', '.cmd'}
        return any(file_path.endswith(ext) for ext in executable_extensions)
    
    def get_available_template_types(self) -> List[TemplateType]:
        """
        Get list of available template types.
        
        Returns:
            List[TemplateType]: Available template types
        """
        return list(TemplateType)
    
    def clear_cache(self):
        """Clear the template cache."""
        self._template_cache.clear()