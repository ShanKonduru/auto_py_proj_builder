"""
Input validation utilities for Python Framework Generator.
Provides validation for user inputs and configuration.
"""
import re
from pathlib import Path
from typing import List, Optional


class InputValidator:
    """
    Validates user inputs for project generation.
    
    Provides methods to validate project names, emails, versions,
    and other user-provided data.
    """
    
    # Regex patterns for validation
    PROJECT_NAME_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]*$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PYTHON_VERSION_PATTERN = re.compile(r'^\d+\.\d+$')
    PACKAGE_NAME_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]*$')
    
    def __init__(self):
        """Initialize validator."""
        self.reserved_names = {
            # Python built-in modules
            'os', 'sys', 'json', 'time', 'datetime', 'pathlib', 'collections',
            'itertools', 'functools', 'operator', 'typing', 'abc', 'enum',
            'dataclasses', 'contextlib', 'logging', 'unittest', 'pytest',
            
            # Common package names to avoid conflicts
            'test', 'tests', 'main', 'setup', 'config', 'utils', 'lib',
            'src', 'dist', 'build', 'docs', 'examples', 'scripts'
        }
    
    def is_valid_project_name(self, name: str) -> bool:
        """
        Validate project name.
        
        Project names must:
        - Start with a letter
        - Contain only letters, numbers, underscores, and hyphens
        - Not be a reserved name
        - Be between 1 and 100 characters
        
        Args:
            name: Project name to validate
            
        Returns:
            bool: True if valid
        """
        if not name or len(name) > 100:
            return False
        
        if name.lower() in self.reserved_names:
            return False
        
        return bool(self.PROJECT_NAME_PATTERN.match(name))
    
    def is_valid_email(self, email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if valid format
        """
        if not email or len(email) > 254:  # RFC 5321 limit
            return False
        
        return bool(self.EMAIL_PATTERN.match(email))
    
    def is_valid_python_version(self, version: str) -> bool:
        """
        Validate Python version format.
        
        Accepts formats like: 3.9, 3.10, 3.11
        
        Args:
            version: Python version string
            
        Returns:
            bool: True if valid format
        """
        if not version:
            return False
        
        if not self.PYTHON_VERSION_PATTERN.match(version):
            return False
        
        # Check that it's a reasonable Python version
        try:
            major, minor = map(int, version.split('.'))
            return major == 3 and 6 <= minor <= 15  # Python 3.6 to 3.15
        except ValueError:
            return False
    
    def is_valid_package_name(self, name: str) -> bool:
        """
        Validate Python package name.
        
        Package names must follow Python identifier rules.
        
        Args:
            name: Package name to validate
            
        Returns:
            bool: True if valid
        """
        if not name or len(name) > 100:
            return False
        
        return bool(self.PACKAGE_NAME_PATTERN.match(name))
    
    def is_valid_dependency_list(self, dependencies: str) -> bool:
        """
        Validate comma-separated dependency list.
        
        Args:
            dependencies: Comma-separated package names
            
        Returns:
            bool: True if all dependencies are valid
        """
        if not dependencies:
            return True
        
        dep_list = [dep.strip() for dep in dependencies.split(',')]
        return all(self.is_valid_package_name(dep) for dep in dep_list if dep)
    
    def is_valid_path(self, path: str) -> bool:
        """
        Validate file system path.
        
        Args:
            path: File system path
            
        Returns:
            bool: True if valid path format
        """
        if not path:
            return False
        
        try:
            # Try to create Path object to validate format
            path_obj = Path(path)
            
            # Check for invalid characters (basic check)
            invalid_chars = '<>"|?*'
            if any(char in path for char in invalid_chars):
                return False
            
            return True
        except (ValueError, OSError):
            return False
    
    def is_safe_directory_name(self, name: str) -> bool:
        """
        Check if directory name is safe to create.
        
        Args:
            name: Directory name
            
        Returns:
            bool: True if safe
        """
        if not name:
            return False
        
        # Check for reserved names on Windows
        windows_reserved = {
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        }
        
        if name.upper() in windows_reserved:
            return False
        
        # Check for invalid characters
        invalid_chars = '<>:"/\\|?*'
        if any(char in name for char in invalid_chars):
            return False
        
        # Check for names that start/end with spaces or dots
        if name.startswith(' ') or name.endswith(' '):
            return False
        
        if name.startswith('.') or name.endswith('.'):
            return False
        
        return True
    
    def validate_template_type(self, template_type: str) -> bool:
        """
        Validate template type.
        
        Args:
            template_type: Template type string
            
        Returns:
            bool: True if valid
        """
        valid_types = {'basic', 'cli', 'web', 'library'}
        return template_type.lower() in valid_types
    
    def validate_coverage_threshold(self, threshold: int) -> bool:
        """
        Validate coverage threshold value.
        
        Args:
            threshold: Coverage threshold percentage
            
        Returns:
            bool: True if valid (0-100)
        """
        return isinstance(threshold, int) and 0 <= threshold <= 100
    
    def get_validation_errors(self, **kwargs) -> List[str]:
        """
        Get list of validation errors for multiple inputs.
        
        Args:
            **kwargs: Key-value pairs to validate
            
        Returns:
            List[str]: List of validation error messages
        """
        errors = []
        
        # Validate project name
        if 'project_name' in kwargs:
            if not self.is_valid_project_name(kwargs['project_name']):
                errors.append("Invalid project name format")
        
        # Validate email
        if 'email' in kwargs and kwargs['email']:
            if not self.is_valid_email(kwargs['email']):
                errors.append("Invalid email address format")
        
        # Validate Python version
        if 'python_version' in kwargs:
            if not self.is_valid_python_version(kwargs['python_version']):
                errors.append("Invalid Python version format")
        
        # Validate dependencies
        if 'dependencies' in kwargs and kwargs['dependencies']:
            if not self.is_valid_dependency_list(kwargs['dependencies']):
                errors.append("Invalid dependency list format")
        
        # Validate target path
        if 'target_path' in kwargs:
            if not self.is_valid_path(kwargs['target_path']):
                errors.append("Invalid target path")
        
        # Validate coverage threshold
        if 'coverage_threshold' in kwargs:
            if not self.validate_coverage_threshold(kwargs['coverage_threshold']):
                errors.append("Coverage threshold must be between 0 and 100")
        
        return errors
    
    def sanitize_project_name(self, name: str) -> str:
        """
        Sanitize project name by removing invalid characters.
        
        Args:
            name: Original project name
            
        Returns:
            str: Sanitized project name
        """
        if not name:
            return "unnamed_project"
        
        # Remove invalid characters
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        
        # Ensure it starts with a letter
        if not sanitized[0].isalpha():
            sanitized = 'project_' + sanitized
        
        # Remove consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        
        # Remove trailing underscores
        sanitized = sanitized.rstrip('_')
        
        # Ensure it's not empty
        if not sanitized:
            sanitized = "unnamed_project"
        
        return sanitized
    
    def suggest_alternatives(self, name: str) -> List[str]:
        """
        Suggest alternative project names if current one is invalid.
        
        Args:
            name: Original project name
            
        Returns:
            List[str]: List of suggested alternatives
        """
        suggestions = []
        
        if name.lower() in self.reserved_names:
            suggestions.extend([
                f"my_{name}",
                f"{name}_project",
                f"{name}_app",
                f"custom_{name}"
            ])
        
        if not self.is_valid_project_name(name):
            sanitized = self.sanitize_project_name(name)
            suggestions.append(sanitized)
            
            # Add some variations
            suggestions.extend([
                f"{sanitized}_app",
                f"my_{sanitized}",
                f"{sanitized}_tool"
            ])
        
        return list(set(suggestions))  # Remove duplicates