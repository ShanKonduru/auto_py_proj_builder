"""
Generate command implementation for Python Framework Generator CLI.
"""
import click
from pathlib import Path
from typing import Optional

from models.project_template import ProjectTemplate, TemplateType
from models.project_metadata import ProjectMetadata
from models.configuration_profile import ConfigurationProfile, ProfileType
from services.project_generator import ProjectGenerator
from utils.validation import InputValidator


@click.command()
@click.argument('name', required=False)
@click.option('--name', '-n', 'name_option',
              help='Project name (can also be provided as first argument)')
@click.option('--type', '-t', '--template',
              'template_type',
              type=click.Choice([t.value for t in TemplateType]),
              default=TemplateType.BASIC.value,
              help='Project template type')
@click.option('--path', '-p', '--output-dir',
              type=click.Path(path_type=Path),
              help='Target directory path (default: current directory)')
@click.option('--author', '-a',
              help='Author name')
@click.option('--email', '-e',
              help='Author email')
@click.option('--description', '-d',
              help='Project description')
@click.option('--python-version',
              default='3.9',
              help='Minimum Python version (default: 3.9)')
@click.option('--dependencies',
              help='Comma-separated list of additional dependencies')
@click.option('--include-tests/--no-tests',
              default=True,
              help='Include test configuration (default: yes)')
@click.option('--include-linting/--no-linting',
              default=True,
              help='Include linting configuration (default: yes)')
@click.option('--coverage-threshold',
              type=int,
              default=90,
              help='Coverage fail-under threshold (default: 90)')
@click.option('--include-batch-files/--no-batch-files',
              default=True,
              help='Include batch files for development workflow (default: yes)')
@click.option('--force', '-f',
              is_flag=True,
              help='Overwrite existing directory')
@click.option('--dry-run',
              is_flag=True,
              help='Show what would be generated without creating files')
@click.option('--verbose', '-v',
              is_flag=True,
              help='Verbose output')
def generate(name: Optional[str],
             name_option: Optional[str],
             template_type: str,
             path: Optional[Path],
             author: Optional[str],
             email: Optional[str],
             description: Optional[str],
             python_version: str,
             dependencies: Optional[str],
             include_tests: bool,
             include_linting: bool,
             coverage_threshold: int,
             include_batch_files: bool,
             force: bool,
             dry_run: bool,
             verbose: bool):
    """
    Generate a new Python project from templates.
    
    Creates a new project with the specified configuration including
    source structure, tests, configuration files, and documentation.
    
    Examples:
    
        # Generate a basic project
        python-generator generate --name myproject
        
        # Generate a CLI project with specific configuration
        python-generator generate --name mycli --type cli --author "John Doe"
        
        # Generate a web project with custom dependencies
        python-generator generate --name myweb --type web --dependencies "fastapi,uvicorn"
    """
    try:
        # Resolve project name (from argument or option)
        project_name = name or name_option
        if not project_name:
            raise click.BadParameter("Project name is required (use first argument or --name option)")
        
        # Initialize validator
        validator = InputValidator()
        
        # Validate inputs
        if verbose:
            click.echo("Validating inputs...")
        
        _validate_inputs(validator, project_name, author, email, python_version, 
                        coverage_threshold, dependencies)
        
        # Set defaults from environment or prompts
        if not author:
            author = click.prompt('Author name', default='Developer')
        
        if not email:
            email = click.prompt('Author email', default='developer@example.com')
        
        if not description:
            description = f'A {template_type} Python project'
        
        # Parse dependencies
        dependency_list = _parse_dependencies(dependencies)
        
        # Determine project path
        target_path = path or Path.cwd() / project_name
        
        # Check for existing directory
        if target_path.exists() and not force:
            if not click.confirm(f'Directory {target_path} exists. Continue?'):
                click.echo('Generation cancelled.')
                return
        
        # Create project template
        project_template = ProjectTemplate(
            name=f"{project_name}_template",
            template_type=TemplateType(template_type),
            description=f"Template for {project_name}",
            author=author,
            email=email,
            python_version=python_version,
            include_batch_files=include_batch_files
        )
        
        # Create project metadata
        project_metadata = ProjectMetadata(
            project_name=project_name,
            target_directory=str(target_path),
            author_info={'name': author, 'email': email},
            dependencies=dependency_list
        )
        
        # Create configuration profile  
        profile_type = ProfileType.BASIC
        if not include_tests and not include_linting:
            profile_type = ProfileType.MINIMAL
        elif include_tests and include_linting:
            profile_type = ProfileType.ADVANCED
            
        configuration_profile = ConfigurationProfile(
            profile_type=profile_type
        )
        
        # Update coverage settings if needed
        if include_tests and coverage_threshold != 90:
            configuration_profile.coverage_settings['fail_under'] = coverage_threshold
        
        # Show generation plan
        if verbose or dry_run:
            _show_generation_plan(project_template, project_metadata, 
                                  configuration_profile, target_path)
        
        if dry_run:
            click.echo("Dry run complete. No files were created.")
            return
        
        # Generate project
        if verbose:
            click.echo("Starting project generation...")
        
        generator = ProjectGenerator()
        success = generator.generate(
            project_template=project_template,
            project_metadata=project_metadata,
            configuration_profile=configuration_profile
        )
        
        if success:
            click.echo(f"✅ Successfully generated project '{project_name}' in {target_path}")
            _show_next_steps(project_name, target_path, template_type)
        else:
            click.echo("❌ Project generation failed", err=True)
            raise click.ClickException("Generation failed")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        raise click.ClickException(str(e))


def _validate_inputs(validator: InputValidator,
                    name: str,
                    author: Optional[str],
                    email: Optional[str],
                    python_version: str,
                    coverage_threshold: int,
                    dependencies: Optional[str]):
    """Validate user inputs."""
    # Validate project name
    if not validator.is_valid_project_name(name):
        raise click.BadParameter(
            "Project name must contain only letters, numbers, underscores, and hyphens"
        )
    
    # Validate email if provided
    if email and not validator.is_valid_email(email):
        raise click.BadParameter("Invalid email format")
    
    # Validate Python version
    if not validator.is_valid_python_version(python_version):
        raise click.BadParameter(
            "Python version must be in format X.Y (e.g., 3.9, 3.10)"
        )
    
    # Validate coverage threshold
    if not (0 <= coverage_threshold <= 100):
        raise click.BadParameter(
            "Coverage threshold must be between 0 and 100"
        )
    
    # Validate dependencies format
    if dependencies and not validator.is_valid_dependency_list(dependencies):
        raise click.BadParameter(
            "Dependencies must be comma-separated package names"
        )


def _parse_dependencies(dependencies: Optional[str]) -> list:
    """Parse dependency string into list."""
    if not dependencies:
        return []
    
    return [dep.strip() for dep in dependencies.split(',') if dep.strip()]


def _get_default_patterns(template_type: TemplateType) -> list:
    """Get default file patterns for template type."""
    base_patterns = [
        "*.py", "*.md", "*.txt", "*.ini", "*.toml", "*.cfg"
    ]
    
    if template_type == TemplateType.CLI:
        base_patterns.extend(["*.sh", "*.bat"])
    elif template_type == TemplateType.WEB:
        base_patterns.extend(["*.html", "*.css", "*.js", "*.json"])
    elif template_type == TemplateType.LIBRARY:
        base_patterns.extend(["*.yml", "*.yaml"])
    
    return base_patterns


def _show_generation_plan(project_template: ProjectTemplate,
                         project_metadata: ProjectMetadata,
                         configuration_profile: ConfigurationProfile,
                         target_path: Path):
    """Show what will be generated."""
    click.echo("\n📋 Generation Plan:")
    click.echo(f"  Project Name: {project_metadata.project_name}")
    click.echo(f"  Template Type: {project_template.template_type.value}")
    click.echo(f"  Target Path: {target_path}")
    click.echo(f"  Author: {project_metadata.author_info['name']} <{project_metadata.author_info['email']}>")
    click.echo(f"  Python Version: {project_template.python_version}+")
    
    if project_metadata.dependencies:
        click.echo(f"  Dependencies: {', '.join(project_metadata.dependencies)}")
    
    click.echo(f"  Profile Type: {configuration_profile.profile_type.value}")
    
    if configuration_profile.coverage_settings:
        threshold = configuration_profile.coverage_settings.get('fail_under', 90)
        click.echo(f"  Coverage Threshold: {threshold}%")
    
    click.echo()


def _show_next_steps(project_name: str, target_path: Path, template_type: str):
    """Show next steps after successful generation."""
    click.echo("\n🎉 Next Steps:")
    click.echo(f"  1. cd {target_path}")
    click.echo("  2. python -m venv venv")
    
    # Platform-specific activation command
    import platform
    if platform.system() == "Windows":
        click.echo("  3. venv\\Scripts\\activate")
    else:
        click.echo("  3. source venv/bin/activate")
    
    click.echo("  4. pip install -r requirements.txt")
    
    if template_type == "cli":
        click.echo("  5. python main.py --help")
    elif template_type == "web":
        click.echo("  5. python main.py")
    else:
        click.echo("  5. python main.py")
    
    click.echo("  6. pytest (to run tests)")
    click.echo("\n📖 See README.md for detailed instructions.")


# Make the command available for import
__all__ = ['generate']