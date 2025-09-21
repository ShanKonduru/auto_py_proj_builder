"""
ProjectMetadata model for Python Framework Generator.
Represents user-provided information for project customization.
"""
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ProjectMetadata:
    """
    Represents user-provided information for project customization.
    
    Attributes:
        project_name: User-specified project name
        target_directory: Directory where project will be created
        author_info: Author name and email information
        custom_markers: Additional pytest markers to include
        dependencies: Custom dependencies beyond defaults
    """
    project_name: str
    target_directory: str
    author_info: Dict[str, str] = field(default_factory=dict)
    custom_markers: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization validation and setup."""
        # Set default author info structure
        if not self.author_info:
            self.author_info = {'name': '', 'email': ''}
        
        # Ensure author_info has required keys
        if 'name' not in self.author_info:
            self.author_info['name'] = ''
        if 'email' not in self.author_info:
            self.author_info['email'] = ''
        
        self.validate()
    
    def validate(self) -> bool:
        """
        Validate project metadata.
        
        Returns:
            bool: True if validation passes
            
        Raises:
            ValueError: If validation fails
        """
        # Validate project name
        if not self.project_name:
            raise ValueError("Project name cannot be empty")
        
        if not self.project_name.replace('_', '').replace('-', '').isalnum():
            raise ValueError(
                "Project name must contain only letters, numbers, hyphens, and underscores"
            )
        
        # Validate target directory
        if not self.target_directory:
            raise ValueError("Target directory cannot be empty")
        
        # Check if target directory is writable
        if not self._is_directory_writable(self.target_directory):
            raise ValueError(f"Target directory '{self.target_directory}' is not writable")
        
        # Check for project name conflicts
        project_path = Path(self.target_directory) / self.project_name
        if project_path.exists():
            raise ValueError(
                f"Project directory '{project_path}' already exists. "
                "Choose a different name or location."
            )
        
        # Validate dependencies
        for dependency in self.dependencies:
            if not self._is_valid_package_name(dependency):
                raise ValueError(f"Invalid package name: '{dependency}'")
        
        # Validate custom markers
        for marker in self.custom_markers:
            if not self._is_valid_marker_name(marker):
                raise ValueError(f"Invalid marker name: '{marker}'")
        
        return True
    
    def _is_directory_writable(self, directory: str) -> bool:
        """
        Check if directory is writable.
        
        Args:
            directory: Directory path to check
            
        Returns:
            bool: True if directory is writable
        """
        try:
            dir_path = Path(directory)
            
            # If directory doesn't exist, check parent directory
            if not dir_path.exists():
                # Try to create it temporarily
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    # If we created it, remove it for now
                    if dir_path.exists():
                        dir_path.rmdir()
                    return True
                except (OSError, PermissionError):
                    return False
            
            # Directory exists, check if writable
            return os.access(directory, os.W_OK)
            
        except (OSError, PermissionError):
            return False
    
    def _is_valid_package_name(self, package_name: str) -> bool:
        """
        Check if package name is valid.
        
        Args:
            package_name: Package name to validate
            
        Returns:
            bool: True if valid package name
        """
        if not package_name:
            return False
        
        # Allow package names with version specifiers (e.g., 'click>=8.0')
        import re
        
        # Basic pattern for package names (letters, numbers, hyphens, underscores, dots)
        # Can include version specifiers like >=, ==, !=, etc.
        pattern = r'^[a-zA-Z0-9_.-]+([><=!]+[0-9.]+[a-zA-Z0-9]*)?$'
        return bool(re.match(pattern, package_name))
    
    def _is_valid_marker_name(self, marker: str) -> bool:
        """
        Check if pytest marker name is valid.
        
        Args:
            marker: Marker name to validate
            
        Returns:
            bool: True if valid marker name
        """
        if not marker:
            return False
        
        # Marker names should be valid Python identifiers
        return marker.isidentifier()
    
    def get_project_path(self) -> Path:
        """
        Get the full path where the project will be created.
        
        Returns:
            Path: Full project path
        """
        return Path(self.target_directory) / self.project_name
    
    def get_author_name(self) -> str:
        """
        Get author name with fallback.
        
        Returns:
            str: Author name or default
        """
        return self.author_info.get('name', 'Unknown Author')
    
    def get_author_email(self) -> str:
        """
        Get author email with fallback.
        
        Returns:
            str: Author email or empty string
        """
        return self.author_info.get('email', '')
    
    def add_dependency(self, dependency: str) -> None:
        """
        Add a dependency to the list.
        
        Args:
            dependency: Package dependency to add
            
        Raises:
            ValueError: If dependency is invalid
        """
        if not self._is_valid_package_name(dependency):
            raise ValueError(f"Invalid package name: '{dependency}'")
        
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)
    
    def add_custom_marker(self, marker: str) -> None:
        """
        Add a custom pytest marker.
        
        Args:
            marker: Marker name to add
            
        Raises:
            ValueError: If marker name is invalid
        """
        if not self._is_valid_marker_name(marker):
            raise ValueError(f"Invalid marker name: '{marker}'")
        
        if marker not in self.custom_markers:
            self.custom_markers.append(marker)
    
    def get_template_context(self) -> dict:
        """
        Get context dictionary for template rendering.
        
        Returns:
            dict: Context for template rendering
        """
        return {
            'project_name': self.project_name,
            'target_directory': self.target_directory,
            'author_name': self.get_author_name(),
            'author_email': self.get_author_email(),
            'custom_markers': self.custom_markers,
            'dependencies': self.dependencies,
            'project_path': str(self.get_project_path())
        }
    
    def to_dict(self) -> dict:
        """
        Convert metadata to dictionary.
        
        Returns:
            dict: Metadata as dictionary
        """
        return {
            'project_name': self.project_name,
            'target_directory': self.target_directory,
            'author_info': self.author_info,
            'custom_markers': self.custom_markers,
            'dependencies': self.dependencies,
            'project_path': str(self.get_project_path())
        }