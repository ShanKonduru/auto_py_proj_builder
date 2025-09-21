"""
Integration tests for installation verification.
Tests the overall installation and basic functionality.
"""
import pytest
import subprocess
import sys
from click.testing import CliRunner

# Imports will fail initially - expected for TDD
try:
    from cli.main import main
except ImportError:
    def main():
        pass


class TestInstallationVerification:
    """Test installation and basic functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.runner = CliRunner()
    
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_main_command_available(self):
        """Test that main command is accessible."""
        result = self.runner.invoke(main, ['--help'])
        # Will initially fail - no implementation
        assert result.exit_code == 0
        assert 'python-framework-gen' in result.output or 'generate' in result.output
    
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_help_command_shows_usage(self):
        """Test that help command displays usage information."""
        result = self.runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        
        # Should show available commands and options
        help_text = result.output.lower()
        assert 'usage' in help_text or 'commands' in help_text
        assert 'generate' in help_text
    
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_version_information_available(self):
        """Test that version information is available."""
        result = self.runner.invoke(main, ['--version'])
        
        # Should show version or at least not error
        assert result.exit_code == 0
        # Version should contain numbers or version-like pattern
        assert any(char.isdigit() for char in result.output)
    
    @pytest.mark.integration
    def test_generate_subcommand_available(self):
        """Test that generate subcommand is available."""
        result = self.runner.invoke(main, ['generate', '--help'])
        assert result.exit_code == 0
        
        help_text = result.output
        # Should show generate command options
        assert 'PROJECT_NAME' in help_text or 'project' in help_text.lower()
        assert '--author' in help_text
        assert '--template' in help_text
    
    @pytest.mark.integration
    def test_error_handling_for_invalid_commands(self):
        """Test graceful error handling for invalid commands."""
        result = self.runner.invoke(main, ['invalid_command'])
        
        # Should fail gracefully with helpful error
        assert result.exit_code != 0
        assert 'invalid' in result.output.lower() or 'usage' in result.output.lower()
    
    @pytest.mark.integration
    def test_python_import_structure(self):
        """Test that Python package structure can be imported."""
        # This test verifies the package structure is importable
        # Will initially fail due to missing implementation
        
        try:
            # These imports should work once implemented
            from src.models import project_template
            from src.services import project_generator
            from src.cli import main
            from src.utils import validation
            import_success = True
        except ImportError:
            import_success = False
        
        # This assertion will initially fail, driving implementation
        assert import_success, "Core package modules should be importable"
    
    @pytest.mark.integration
    def test_dependencies_available(self):
        """Test that required dependencies are available."""
        required_dependencies = ['click', 'jinja2', 'pathlib']
        
        for dependency in required_dependencies:
            try:
                __import__(dependency)
                dependency_available = True
            except ImportError:
                dependency_available = False
            
            assert dependency_available, f"Required dependency {dependency} not available"
    
    @pytest.mark.integration
    def test_pytest_configuration_working(self):
        """Test that pytest configuration is working correctly."""
        # This test should run and collect without configuration errors
        
        # Try to run pytest on the test suite itself
        result = subprocess.run([
            sys.executable, '-m', 'pytest', '--collect-only', '-q'
        ], capture_output=True, text=True)
        
        # Should be able to collect tests without configuration errors
        assert 'error' not in result.stderr.lower()
        assert result.returncode == 0
    
    @pytest.mark.integration
    def test_markers_configuration(self):
        """Test that pytest markers are properly configured."""
        # Run pytest with marker list to verify configuration
        result = subprocess.run([
            sys.executable, '-m', 'pytest', '--markers'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        
        # Should list our custom markers
        markers_output = result.stdout
        expected_markers = ['integration', 'contract', 'performance', 'unit', 'slow']
        
        for marker in expected_markers:
            assert marker in markers_output, f"Marker {marker} not found in pytest configuration"
    
    @pytest.mark.integration 
    @pytest.mark.slow
    def test_end_to_end_basic_workflow(self):
        """Test complete end-to-end basic workflow."""
        # This is a comprehensive test that exercises the full workflow
        import tempfile
        import shutil
        from pathlib import Path
        
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)
        
        try:
            # Test complete workflow: install -> help -> generate -> verify
            
            # 1. Help should work
            help_result = self.runner.invoke(main, ['--help'])
            assert help_result.exit_code == 0
            
            # 2. Generate a project
            result = self.runner.invoke(main, [
                'generate', 'test_e2e_project',
                '--output-dir', str(temp_path),
                '--author', 'E2E Test',
                '--email', 'e2e@test.com',
                '--template', 'basic'
            ])
            
            # This will initially fail - no implementation
            assert result.exit_code == 0
            
            # 3. Verify project was created
            project_path = temp_path / 'test_e2e_project'
            assert project_path.exists()
            
            # 4. Verify project structure is valid
            required_files = ['main.py', 'requirements.txt', 'README.md']
            for file_name in required_files:
                assert (project_path / file_name).exists()
            
            # 5. Verify generated project is functional
            # (Try to run pytest on the generated project)
            pytest_result = subprocess.run([
                sys.executable, '-m', 'pytest', '--collect-only'
            ], cwd=str(project_path), capture_output=True, text=True)
            
            # Should be able to collect tests without errors
            assert pytest_result.returncode == 0
            
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)