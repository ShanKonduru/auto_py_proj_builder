"""
ProjectGenerator service for Python Framework Generator.
Core service that orchestrates project generation.
"""
import os
import platform
from pathlib import Path
from typing import Dict, List, Optional

from models.project_template import ProjectTemplate, ProjectState
from models.project_metadata import ProjectMetadata
from models.template_file import TemplateFile
from models.configuration_profile import ConfigurationProfile
from services.template_loader import TemplateLoader
from services.filesystem_service import FileSystemService


class ProjectGenerator:
    """
    Core service that orchestrates project generation.
    
    Coordinates template loading, file generation, and project setup.
    """
    
    def __init__(self, 
                 template_loader: Optional[TemplateLoader] = None,
                 filesystem_service: Optional[FileSystemService] = None):
        """
        Initialize project generator.
        
        Args:
            template_loader: Service for loading templates
            filesystem_service: Service for file operations
        """
        self.template_loader = template_loader or TemplateLoader()
        self.filesystem_service = filesystem_service or FileSystemService()
        self.current_platform = platform.system().lower()
    
    def generate(self, 
                 project_template: ProjectTemplate,
                 project_metadata: ProjectMetadata,
                 configuration_profile: Optional[ConfigurationProfile] = None) -> bool:
        """
        Generate a complete project based on templates and metadata.
        
        Args:
            project_template: Project template configuration
            project_metadata: User-provided project information
            configuration_profile: Quality and testing configuration
            
        Returns:
            bool: True if generation successful
            
        Raises:
            ValueError: If generation fails
        """
        try:
            # Validate inputs
            project_template.validate()
            project_metadata.validate()
            
            # Use default configuration if not provided
            if configuration_profile is None:
                configuration_profile = ConfigurationProfile()
            
            # Load templates
            template_files = self.template_loader.load_templates_for_type(
                project_template.template_type
            )
            
            # Create project directory
            project_path = project_metadata.get_project_path()
            self.filesystem_service.create_directory(project_path)
            
            # Prepare template context
            context = self._prepare_template_context(
                project_template, project_metadata, configuration_profile
            )
            
            # Generate files
            generated_files = self._generate_files(
                template_files, project_path, context
            )
            
            # Create configuration files
            self._create_configuration_files(
                project_path, configuration_profile, context
            )
            
            # Set file permissions
            self._set_file_permissions(generated_files, project_path)
            
            # Mark as generated
            project_template.mark_generated()
            
            # Validate generated project
            if self._validate_generated_project(project_path):
                project_template.mark_completed()
                return True
            else:
                raise ValueError("Generated project failed validation")
                
        except Exception as e:
            # Cleanup on failure
            if project_metadata.get_project_path().exists():
                self.filesystem_service.remove_directory(
                    project_metadata.get_project_path()
                )
            raise ValueError(f"Project generation failed: {str(e)}")
    
    def _prepare_template_context(self,
                                  project_template: ProjectTemplate,
                                  project_metadata: ProjectMetadata,
                                  configuration_profile: ConfigurationProfile) -> Dict:
        """
        Prepare context for template rendering.
        
        Args:
            project_template: Project template
            project_metadata: Project metadata
            configuration_profile: Configuration profile
            
        Returns:
            dict: Template rendering context
        """
        context = {}
        
        # Add project template data
        context.update(project_template.to_dict())
        
        # Add project metadata
        context.update(project_metadata.get_template_context())
        
        # Add configuration data
        context.update({
            'pytest_markers': configuration_profile.pytest_markers,
            'quality_tools': configuration_profile.quality_tools,
            'coverage_fail_under': configuration_profile.coverage_settings.get('fail_under', 50)
        })
        
        # Add system information
        context.update({
            'python_executable': 'python',
            'current_platform': self.current_platform,
            'is_windows': self.current_platform == 'windows'
        })
        
        return context
    
    def _generate_files(self,
                       template_files: List[TemplateFile],
                       project_path: Path,
                       context: Dict) -> List[Path]:
        """
        Generate all project files from templates.
        
        Args:
            template_files: List of template files
            project_path: Target project directory
            context: Template rendering context
            
        Returns:
            List[Path]: List of generated file paths
        """
        generated_files = []
        
        for template_file in template_files:
            # Check platform compatibility
            if not template_file.should_include_for_platform(self.current_platform):
                continue
            
            # Skip batch files if not requested
            if (template_file.file_path.endswith('.bat') and 
                not context.get('include_batch_files', True)):
                continue
            
            # Generate file
            file_path = self._generate_single_file(
                template_file, project_path, context
            )
            
            if file_path:
                generated_files.append(file_path)
        
        return generated_files
    
    def _generate_single_file(self,
                             template_file: TemplateFile,
                             project_path: Path,
                             context: Dict) -> Optional[Path]:
        """
        Generate a single file from template.
        
        Args:
            template_file: Template file to generate
            project_path: Target project directory
            context: Template rendering context
            
        Returns:
            Optional[Path]: Generated file path or None if failed
        """
        try:
            # Render template content
            rendered_content = template_file.render_content(context)
            
            # Get target file path
            target_path = template_file.get_absolute_path(project_path)
            
            # Create parent directories
            self.filesystem_service.create_directory(target_path.parent)
            
            # Write file
            self.filesystem_service.write_file(target_path, rendered_content)
            
            return target_path
            
        except Exception as e:
            print(f"Warning: Failed to generate {template_file.file_path}: {str(e)}")
            return None
    
    def _create_configuration_files(self,
                                   project_path: Path,
                                   configuration_profile: ConfigurationProfile,
                                   context: Dict):
        """
        Create configuration files (pytest.ini, pyproject.toml, etc.).
        
        Args:
            project_path: Target project directory
            configuration_profile: Configuration profile
            context: Template rendering context
        """
        # Create pytest.ini
        pytest_config = configuration_profile.get_pytest_config()
        pytest_content = self._format_pytest_ini(pytest_config)
        pytest_path = project_path / 'pytest.ini'
        self.filesystem_service.write_file(pytest_path, pytest_content)
        
        # Create or update pyproject.toml
        pyproject_content = self._create_pyproject_toml(configuration_profile, context)
        pyproject_path = project_path / 'pyproject.toml'
        self.filesystem_service.write_file(pyproject_path, pyproject_content)
    
    def _format_pytest_ini(self, config: Dict) -> str:
        """Format pytest configuration as INI file."""
        lines = ['[tool:pytest]']
        
        # Add simple key-value pairs
        for key, value in config.items():
            if key == 'markers':
                continue  # Handle markers separately
            if isinstance(value, list):
                if key == 'addopts':
                    lines.append(f'{key} = ')
                    for opt in value:
                        lines.append(f'    {opt}')
                else:
                    lines.append(f'{key} = {" ".join(value)}')
            else:
                lines.append(f'{key} = {value}')
        
        # Add markers
        if 'markers' in config:
            lines.append('markers =')
            for marker in config['markers']:
                lines.append(f'    {marker}')
        
        return '\n'.join(lines) + '\n'
    
    def _create_pyproject_toml(self, 
                              configuration_profile: ConfigurationProfile,
                              context: Dict) -> str:
        """Create pyproject.toml content."""
        project_name = context['project_name']
        author_name = context['author_name']
        author_email = context['author_email']
        python_version = context['python_version']
        
        content = f'''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "{context.get('project_description', '')}"
readme = "README.md"
authors = [{{name = "{author_name}", email = "{author_email}"}}]
license = {{text = "MIT"}}
requires-python = ">={python_version}"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: {python_version}",
]

[project.scripts]
{project_name} = "main:main"
'''
        
        # Add tool configurations
        quality_config = configuration_profile.get_quality_tools_config()
        for tool, config in quality_config.items():
            content += f'\n[tool.{tool}]\n'
            for key, value in config.items():
                if isinstance(value, list):
                    content += f'{key} = {value}\n'
                elif isinstance(value, str):
                    content += f'{key} = "{value}"\n'
                else:
                    content += f'{key} = {value}\n'
        
        return content
    
    def _set_file_permissions(self, file_paths: List[Path], project_path: Path):
        """
        Set appropriate file permissions.
        
        Args:
            file_paths: List of generated file paths
            project_path: Project directory path
        """
        for file_path in file_paths:
            if file_path.suffix in {'.sh', '.bat', '.cmd'}:
                self.filesystem_service.make_executable(file_path)
    
    def _validate_generated_project(self, project_path: Path) -> bool:
        """
        Validate that the generated project is complete and correct.
        
        Args:
            project_path: Project directory path
            
        Returns:
            bool: True if project is valid
        """
        required_files = ['main.py', 'requirements.txt', 'README.md']
        
        for file_name in required_files:
            file_path = project_path / file_name
            if not file_path.exists():
                return False
        
        # Check that main.py is valid Python
        main_py_path = project_path / 'main.py'
        try:
            with open(main_py_path, 'r') as f:
                content = f.read()
            # Basic syntax check
            compile(content, str(main_py_path), 'exec')
            return True
        except (SyntaxError, FileNotFoundError):
            return False