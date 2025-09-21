"""
Integration tests for basic project generation functionality.
These tests verify end-to-end project generation workflow.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
from click.testing import CliRunner

# Imports will fail initially - expected for TDD
try:
    from src.cli.main import main
    from src.services.project_generator import ProjectGenerator
    from src.models.project_template import ProjectTemplate
except ImportError:
    import click

    # Mock classes for testing
    class ProjectGenerator:
        def generate(self, *args, **kwargs):
            return True

    class ProjectTemplate:
        pass

    @click.group()
    def main():
        """Mock main command for testing"""
        pass

    @main.command()
    @click.argument("project_name")
    @click.option("--template", default="basic")
    @click.option("--author", default="Test Author")
    @click.option("--email", default="test@example.com")
    @click.option("--output-dir", default=".")
    @click.option("--no-batch-files", is_flag=True)
    def generate(project_name, template, author, email, output_dir, no_batch_files):
        """Mock generate command"""
        pass


class TestBasicProjectGeneration:
    """Test basic project generation end-to-end."""

    def setup_method(self):
        """Setup test environment with temporary directory."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def teardown_method(self):
        """Cleanup temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @pytest.mark.integration
    def test_basic_project_structure_creation(self):
        """Test that basic project structure is created correctly."""
        project_name = "test_basic_project"

        result = self.runner.invoke(
            main,
            [
                "generate",
                project_name,
                "--output-dir",
                str(self.temp_path),
                "--author",
                "Test User",
                "--email",
                "test@example.com",
                "--force",
            ],
        )

        # Print output for debugging if test fails
        if result.exit_code != 0:
            print(f"Exit code: {result.exit_code}")
            print(f"Output: {result.output}")
            print(f"Exception: {result.exception}")

        assert result.exit_code == 0

        # Verify project directory structure
        project_path = self.temp_path / project_name
        assert project_path.exists()
        assert project_path.is_dir()

        # Check for required files
        required_files = [
            "main.py",
            "requirements.txt",
            "pytest.ini",
            "README.md",
            "pyproject.toml",
        ]

        for file_name in required_files:
            file_path = project_path / file_name
            assert file_path.exists(), f"Required file {file_name} not found"

    @pytest.mark.integration
    def test_requirements_txt_content(self):
        """Test that requirements.txt contains expected dependencies."""
        project_name = "test_requirements"

        result = self.runner.invoke(
            main,
            [
                "generate",
                project_name,
                "--output-dir",
                str(self.temp_path),
                "--author",
                "Test Author",
                "--email",
                "test@example.com",
                "--force",
            ],
        )

        # Print output for debugging if test fails
        if result.exit_code != 0:
            print(f"Exit code: {result.exit_code}")
            print(f"Output: {result.output}")
            print(f"Exception: {result.exception}")

        assert result.exit_code == 0

        requirements_path = self.temp_path / project_name / "requirements.txt"
        assert requirements_path.exists()

        content = requirements_path.read_text()
        # Basic template should include pytest
        assert "pytest" in content

    @pytest.mark.integration
    def test_pytest_ini_configuration(self):
        """Test that pytest.ini is configured with markers."""
        project_name = "test_pytest_config"

        result = self.runner.invoke(
            main, ["generate", project_name, "--output-dir", str(self.temp_path), "--force"]
        )

        assert result.exit_code == 0

        pytest_ini_path = self.temp_path / project_name / "pytest.ini"
        assert pytest_ini_path.exists()

        content = pytest_ini_path.read_text()
        assert "markers" in content
        assert "testpaths" in content

    @pytest.mark.integration
    def test_readme_contains_project_info(self):
        """Test that README.md contains project information."""
        project_name = "test_readme"
        author_name = "Test Author"

        result = self.runner.invoke(
            main,
            [
                "generate",
                project_name,
                "--output-dir",
                str(self.temp_path),
                "--author",
                author_name,
                "--force",
            ],
        )

        assert result.exit_code == 0

        readme_path = self.temp_path / project_name / "README.md"
        assert readme_path.exists()

        content = readme_path.read_text()
        assert project_name in content
        assert author_name in content

    @pytest.mark.integration
    def test_main_py_is_executable(self):
        """Test that main.py file is created and contains basic structure."""
        project_name = "test_main_py"

        result = self.runner.invoke(
            main, ["generate", project_name, "--output-dir", str(self.temp_path), "--force"]
        )

        assert result.exit_code == 0

        main_py_path = self.temp_path / project_name / "main.py"
        assert main_py_path.exists()

        content = main_py_path.read_text()
        # Should contain basic Python structure
        assert "def main(" in content or 'if __name__ == "__main__"' in content

    @pytest.mark.integration
    def test_tests_directory_structure(self):
        """Test that tests directory is created with sample test files."""
        project_name = "test_tests_structure"

        result = self.runner.invoke(
            main, ["generate", project_name, "--output-dir", str(self.temp_path), "--force"]
        )

        assert result.exit_code == 0

        tests_path = self.temp_path / project_name / "tests"
        assert tests_path.exists()
        assert tests_path.is_dir()

        # Should contain at least one sample test file
        test_files = list(tests_path.glob("test_*.py"))
        assert len(test_files) > 0

    @pytest.mark.integration
    def test_generated_project_pytest_discovery(self):
        """Test that generated project's tests are discoverable by pytest."""
        project_name = "test_pytest_discovery"

        result = self.runner.invoke(
            main, ["generate", project_name, "--output-dir", str(self.temp_path), "--force"]
        )

        assert result.exit_code == 0

        # This test verifies pytest can discover tests in generated project
        # Will initially fail due to no implementation
        project_path = self.temp_path / project_name

        # Simulate running pytest --collect-only
        # This should discover test files without errors
        from subprocess import run, PIPE

        result = run(
            ["python", "-m", "pytest", "--collect-only", str(project_path)],
            cwd=str(project_path),
            capture_output=True,
            text=True,
        )

        # Should be able to collect tests (even if zero)
        assert "error" not in result.stderr.lower()

    @pytest.mark.integration
    def test_windows_batch_files_generation(self):
        """Test that Windows batch files are generated by default."""
        project_name = "test_batch_files"

        result = self.runner.invoke(
            main, ["generate", project_name, "--output-dir", str(self.temp_path), "--force"]
        )

        assert result.exit_code == 0

        project_path = self.temp_path / project_name

        # Check for Windows batch files
        batch_files = ["run.bat", "test.bat"]
        for batch_file in batch_files:
            batch_path = project_path / batch_file
            # This assertion will initially fail - driving implementation
            assert batch_path.exists(), f"Batch file {batch_file} not generated"

    @pytest.mark.integration
    def test_no_batch_files_flag_respected(self):
        """Test that --no-batch-files flag prevents batch file generation."""
        project_name = "test_no_batch"

        result = self.runner.invoke(
            main,
            [
                "generate",
                project_name,
                "--output-dir",
                str(self.temp_path),
                "--no-batch-files",
                "--force",
            ],
        )

        assert result.exit_code == 0

        project_path = self.temp_path / project_name

        # Should NOT contain batch files
        batch_files = list(project_path.glob("*.bat"))
        assert len(batch_files) == 0
