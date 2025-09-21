"""
Main CLI entry point for Python Framework Generator.
"""
import click
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.generate_command import generate


@click.group()
@click.version_option(version='0.1.0', prog_name='python-generator')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.pass_context
def main(ctx, debug):
    """
    Python Framework Generator - Create Python projects from templates.
    
    A command-line tool for generating structured Python projects with
    best practices, testing configuration, and quality tools.
    
    Examples:
    
        # Generate a basic Python project
        python-generator generate --name myproject
        
        # Generate a CLI application
        python-generator generate --name mycli --type cli
        
        # Generate a web application with custom configuration
        python-generator generate --name myweb --type web --author "John Doe"
    
    For more information, visit: https://github.com/user/python-framework-generator
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    
    if debug:
        click.echo("Debug mode enabled", err=True)


# Add the generate command to the main group
main.add_command(generate)


@main.command()
@click.option('--check-deps', is_flag=True, help='Check if dependencies are available')
def info(check_deps):
    """Show information about the generator and system."""
    import platform
    import sys
    
    click.echo("Python Framework Generator")
    click.echo("=" * 30)
    click.echo(f"Version: 0.1.0")
    click.echo(f"Python: {sys.version}")
    click.echo(f"Platform: {platform.platform()}")
    click.echo(f"Architecture: {platform.architecture()[0]}")
    
    if check_deps:
        click.echo("\nDependency Check:")
        click.echo("-" * 16)
        
        dependencies = [
            ('click', 'CLI framework'),
            ('jinja2', 'Template engine'),
            ('pathlib', 'Path handling (built-in)'),
        ]
        
        for dep_name, description in dependencies:
            try:
                if dep_name == 'pathlib':
                    # pathlib is built-in since Python 3.4
                    status = "✅ Available (built-in)"
                else:
                    __import__(dep_name)
                    status = "✅ Available"
            except ImportError:
                status = "❌ Missing"
            
            click.echo(f"  {dep_name:12} ({description:20}): {status}")


@main.command()
@click.option('--output', '-o', 
              type=click.Path(path_type=Path),
              help='Output file path')
def list_templates(output):
    """List available project templates."""
    from models.project_template import TemplateType
    
    templates = [
        {
            'type': TemplateType.BASIC,
            'name': 'Basic Python Project',
            'description': 'Simple Python project with basic structure'
        },
        {
            'type': TemplateType.CLI,
            'name': 'CLI Application',
            'description': 'Command-line application with Click framework'
        },
        {
            'type': TemplateType.WEB,
            'name': 'Web Application',
            'description': 'Web application with FastAPI or Flask'
        },
        {
            'type': TemplateType.LIBRARY,
            'name': 'Python Library',
            'description': 'Reusable Python library with packaging setup'
        }
    ]
    
    if output:
        # Write to file
        content = "# Available Templates\n\n"
        for template in templates:
            content += f"## {template['name']} (`{template['type'].value}`)\n"
            content += f"{template['description']}\n\n"
        
        with open(output, 'w') as f:
            f.write(content)
        
        click.echo(f"Template list written to {output}")
    else:
        # Display in terminal
        click.echo("Available Templates:")
        click.echo("=" * 20)
        
        for template in templates:
            click.echo(f"\n🔧 {template['name']}")
            click.echo(f"   Type: {template['type'].value}")
            click.echo(f"   Description: {template['description']}")


@main.command()
def validate():
    """Validate the current environment and configuration."""
    import sys
    from pathlib import Path
    
    click.echo("Environment Validation")
    click.echo("=" * 22)
    
    issues = []
    
    # Check Python version
    version_info = sys.version_info
    if version_info < (3, 9):
        issues.append(f"Python {version_info.major}.{version_info.minor} is too old. Requires Python 3.9+")
    else:
        click.echo(f"✅ Python version: {version_info.major}.{version_info.minor}.{version_info.micro}")
    
    # Check write permissions in current directory
    try:
        test_file = Path('.test_write_permission')
        test_file.touch()
        test_file.unlink()
        click.echo("✅ Write permissions: OK")
    except (PermissionError, OSError):
        issues.append("No write permission in current directory")
    
    # Check if we're in a git repository (optional)
    git_dir = Path('.git')
    if git_dir.exists():
        click.echo("ℹ️  Git repository detected")
    
    # Check available disk space (basic check)
    try:
        import shutil
        free_space = shutil.disk_usage('.').free
        if free_space < 100 * 1024 * 1024:  # Less than 100MB
            issues.append("Low disk space (less than 100MB available)")
        else:
            click.echo(f"✅ Disk space: {free_space // (1024*1024)} MB available")
    except OSError:
        click.echo("⚠️  Could not check disk space")
    
    # Summary
    if issues:
        click.echo(f"\n❌ Found {len(issues)} issue(s):")
        for issue in issues:
            click.echo(f"   • {issue}")
        sys.exit(1)
    else:
        click.echo("\n✅ All checks passed! Ready to generate projects.")


def cli():
    """CLI entry point function."""
    try:
        main()
    except KeyboardInterrupt:
        click.echo("\n\nOperation cancelled by user.", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"\n❌ Unexpected error: {str(e)}", err=True)
        import traceback
        if '--debug' in sys.argv:
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    cli()