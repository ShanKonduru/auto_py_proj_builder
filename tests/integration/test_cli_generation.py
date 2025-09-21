"""
Integration tests for CLI-type project generation.
Tests the --template cli option and CLI-specific features.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner

# Imports will fail initially - expected for TDD
try:
    from src.cli.main import main
except ImportError:
    import click
    
    @click.group()
    def main():
        """Mock main command for testing"""
        pass
        
    @main.command()
    @click.argument('project_name')
    @click.option('--template', default='basic')
    @click.option('--author', default='Test Author')
    @click.option('--email', default='test@example.com')
    @click.option('--output-dir', default='.')
    @click.option('--python-version', default='3.9')
    @click.option('--no-batch-files', is_flag=True)
    def generate(project_name, template, author, email, output_dir, python_version, no_batch_files):
        """Mock generate command"""
        pass


class TestCLIProjectGeneration:
    """Test CLI template project generation."""
    
    def setup_method(self):
        """Setup test environment."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @pytest.mark.integration
    def test_cli_template_project_structure(self):
        """Test CLI template generates appropriate project structure."""
        project_name = "my_cli_tool"
        
        result = self.runner.invoke(main, [
            'generate', project_name,
            '--template', 'cli',
            '--output-dir', str(self.temp_path),
            '--author', 'CLI Developer',
            '--python-version', '3.11'
        ])
        
        # Will initially fail - no implementation
        assert result.exit_code == 0
        
        project_path = self.temp_path / project_name
        assert project_path.exists()
        
        # CLI projects should have specific structure
        expected_structure = [
            'main.py',
            'requirements.txt',
            'setup.py',
            'README.md',
            project_name,  # Package directory with project name
            f'{project_name}/cli.py',  # CLI entry point
            f'{project_name}/__init__.py',
            'tests',
            'tests/test_cli.py'
        ]
        
        for expected_path in expected_structure:
            full_path = project_path / expected_path
            assert full_path.exists(), f"Expected CLI structure path not found: {expected_path}"
    
    @pytest.mark.integration
    def test_cli_template_requirements(self):
        """Test CLI template includes Click framework in requirements."""
        project_name = "test_cli_requirements"
        
        result = self.runner.invoke(main, [
            'generate', project_name,
            '--template', 'cli',
            '--output-dir', str(self.temp_path)
        ])
        
        assert result.exit_code == 0
        
        requirements_path = self.temp_path / project_name / 'requirements.txt'
        assert requirements_path.exists()
        
        content = requirements_path.read_text()
        # CLI template should include Click framework
        assert 'click' in content.lower()
    
    @pytest.mark.integration
    def test_cli_template_setup_py_entry_point(self):
        """Test CLI template setup.py includes console script entry point."""
        project_name = "test_cli_setup"
        
        result = self.runner.invoke(main, [
            'generate', project_name,
            '--template', 'cli',
            '--output-dir', str(self.temp_path)
        ])
        
        assert result.exit_code == 0
        
        setup_py_path = self.temp_path / project_name / 'setup.py'
        assert setup_py_path.exists()
        
        content = setup_py_path.read_text()
        # Should include console_scripts entry point
        assert 'console_scripts' in content
        assert 'entry_points' in content
        assert project_name in content
    
    @pytest.mark.integration
    def test_cli_template_main_structure(self):
        """Test CLI template main.py has Click-based structure."""
        project_name = "test_cli_main"
        
        result = self.runner.invoke(main, [
            'generate', project_name,
            '--template', 'cli',
            '--output-dir', str(self.temp_path)
        ])
        
        assert result.exit_code == 0
        
        main_py_path = self.temp_path / project_name / 'main.py'
        assert main_py_path.exists()
        
        content = main_py_path.read_text()
        # Should use Click framework
        assert 'import click' in content
        assert '@click.command' in content or '@click.group' in content
    
    @pytest.mark.integration
    def test_python_version_setting(self):
        """Test custom Python version is set correctly in generated files."""
        project_name = "test_python_version"
        python_version = "3.11"
        
        result = self.runner.invoke(main, [
            'generate', project_name,
            '--template', 'cli',
            '--python-version', python_version,
            '--output-dir', str(self.temp_path)
        ])
        
        assert result.exit_code == 0
        
        setup_py_path = self.temp_path / project_name / 'setup.py'
        content = setup_py_path.read_text()
        
        # Python version should be reflected in setup.py
        assert f'python_requires=">={python_version}"' in content or f'Programming Language :: Python :: {python_version}' in content
    
    @pytest.mark.integration
    def test_no_batch_files_with_cli_template(self):
        """Test --no-batch-files flag works with CLI template."""
        project_name = "test_cli_no_batch"
        
        result = self.runner.invoke(main, [
            'generate', project_name,
            '--template', 'cli',
            '--no-batch-files',
            '--output-dir', str(self.temp_path)
        ])
        
        assert result.exit_code == 0
        
        project_path = self.temp_path / project_name
        
        # Should not contain any .bat files
        batch_files = list(project_path.glob('**/*.bat'))
        assert len(batch_files) == 0
    
    @pytest.mark.integration
    def test_cli_template_test_structure(self):
        """Test CLI template generates appropriate test structure."""
        project_name = "test_cli_tests"
        
        result = self.runner.invoke(main, [
            'generate', project_name,
            '--template', 'cli',
            '--output-dir', str(self.temp_path)
        ])
        
        assert result.exit_code == 0
        
        tests_path = self.temp_path / project_name / 'tests'
        assert tests_path.exists()
        
        # Should have CLI-specific test file
        cli_test_path = tests_path / 'test_cli.py'
        assert cli_test_path.exists()
        
        content = cli_test_path.read_text()
        # Should test Click CLI functionality
        assert 'click' in content.lower() or 'CliRunner' in content
    
    @pytest.mark.integration
    def test_cli_project_name_as_package(self):
        """Test CLI template creates package directory with project name."""
        project_name = "my_awesome_cli"
        
        result = self.runner.invoke(main, [
            'generate', project_name,
            '--template', 'cli',
            '--output-dir', str(self.temp_path)
        ])
        
        assert result.exit_code == 0
        
        # Should create package directory with project name
        package_path = self.temp_path / project_name / project_name
        assert package_path.exists()
        assert package_path.is_dir()
        
        # Package should have __init__.py
        init_path = package_path / '__init__.py'
        assert init_path.exists()
        
        # Should have cli.py module
        cli_path = package_path / 'cli.py'
        assert cli_path.exists()
    
    @pytest.mark.integration
    def test_author_and_email_in_generated_files(self):
        """Test author and email are properly embedded in generated CLI project."""
        project_name = "test_author_info"
        author_name = "John Doe"
        author_email = "john.doe@example.com"
        
        result = self.runner.invoke(main, [
            'generate', project_name,
            '--template', 'cli',
            '--author', author_name,
            '--email', author_email,
            '--output-dir', str(self.temp_path)
        ])
        
        assert result.exit_code == 0
        
        # Check setup.py contains author info
        setup_py_path = self.temp_path / project_name / 'setup.py'
        setup_content = setup_py_path.read_text()
        assert author_name in setup_content
        assert author_email in setup_content
        
        # Check README contains author info
        readme_path = self.temp_path / project_name / 'README.md'
        readme_content = readme_path.read_text()
        assert author_name in readme_content