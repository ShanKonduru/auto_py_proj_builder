"""
TemplateFile model for Python Framework Generator.
Represents individual file templates within a project structure.
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class PlatformCompatibility(Enum):
    """Platform compatibility options."""
    ALL = "all"
    WINDOWS = "windows"
    UNIX = "unix"


@dataclass
class TemplateFile:
    """
    Represents individual file templates within a project structure.
    
    Attributes:
        file_path: Relative path where file should be created
        template_content: Jinja2 template content
        is_executable: Whether file should have execute permissions
        platform_specific: Platform compatibility (all, windows, unix)
        template_variables: Variables available for template rendering
    """
    file_path: str
    template_content: str
    is_executable: bool = False
    platform_specific: PlatformCompatibility = PlatformCompatibility.ALL
    template_variables: Optional[dict] = None
    
    def __post_init__(self):
        """Post-initialization validation and setup."""
        if self.template_variables is None:
            self.template_variables = {}
        self.validate()
    
    def validate(self) -> bool:
        """
        Validate template file data.
        
        Returns:
            bool: True if validation passes
            
        Raises:
            ValueError: If validation fails
        """
        # Validate file path
        if not self.file_path:
            raise ValueError("File path cannot be empty")
        
        # Check for invalid path characters
        invalid_chars = '<>:"|?*'
        if any(char in self.file_path for char in invalid_chars):
            raise ValueError(f"File path contains invalid characters: {invalid_chars}")
        
        # Validate template content
        if self.template_content is None:
            raise ValueError("Template content cannot be None")
        
        # Convert relative path separators to forward slashes for consistency
        self.file_path = self.file_path.replace('\\', '/')
        
        return True
    
    def should_include_for_platform(self, current_platform: str) -> bool:
        """
        Check if file should be included for the current platform.
        
        Args:
            current_platform: Current platform ('windows', 'linux', 'darwin', etc.)
            
        Returns:
            bool: True if file should be included
        """
        if self.platform_specific == PlatformCompatibility.ALL:
            return True
        elif self.platform_specific == PlatformCompatibility.WINDOWS:
            return current_platform.lower() == 'windows'
        elif self.platform_specific == PlatformCompatibility.UNIX:
            return current_platform.lower() in ['linux', 'darwin', 'unix']
        
        return True
    
    def get_absolute_path(self, base_directory: Path) -> Path:
        """
        Get the absolute path for this file within a base directory.
        
        Args:
            base_directory: Base directory for the project
            
        Returns:
            Path: Absolute path where file should be created
        """
        return base_directory / self.file_path
    
    def render_content(self, context: dict) -> str:
        """
        Render the template content with provided context.
        
        Args:
            context: Context variables for template rendering
            
        Returns:
            str: Rendered template content
        """
        from jinja2 import Template, Environment
        
        # Merge template variables with provided context
        full_context = {**self.template_variables, **context}
        
        try:
            # Create Jinja2 template and render
            env = Environment()
            template = env.from_string(self.template_content)
            return template.render(**full_context)
        except Exception as e:
            raise ValueError(f"Failed to render template for {self.file_path}: {str(e)}")
    
    def get_file_extension(self) -> str:
        """
        Get the file extension.
        
        Returns:
            str: File extension including the dot (e.g., '.py', '.txt')
        """
        return Path(self.file_path).suffix
    
    def get_filename(self) -> str:
        """
        Get just the filename without directory path.
        
        Returns:
            str: Filename only
        """
        return Path(self.file_path).name
    
    def get_directory(self) -> str:
        """
        Get the directory path without filename.
        
        Returns:
            str: Directory path
        """
        return str(Path(self.file_path).parent)
    
    def is_python_file(self) -> bool:
        """
        Check if this is a Python file.
        
        Returns:
            bool: True if file has .py extension
        """
        return self.get_file_extension().lower() == '.py'
    
    def is_configuration_file(self) -> bool:
        """
        Check if this is a configuration file.
        
        Returns:
            bool: True if file is a common configuration file
        """
        config_files = {
            'requirements.txt', 'setup.py', 'pyproject.toml', 'pytest.ini',
            'tox.ini', '.gitignore', 'README.md', 'LICENSE', 'MANIFEST.in'
        }
        return self.get_filename() in config_files
    
    def to_dict(self) -> dict:
        """
        Convert template file to dictionary.
        
        Returns:
            dict: Template file data
        """
        return {
            'file_path': self.file_path,
            'template_content': self.template_content,
            'is_executable': self.is_executable,
            'platform_specific': self.platform_specific.value,
            'template_variables': self.template_variables,
            'file_extension': self.get_file_extension(),
            'filename': self.get_filename(),
            'directory': self.get_directory()
        }