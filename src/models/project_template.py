"""
ProjectTemplate model for Python Framework Generator.
Represents the complete blueprint for generating a Python project.
"""
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class TemplateType(Enum):
    """Project template types."""
    BASIC = "basic"
    WEB = "web"
    CLI = "cli"
    LIBRARY = "library"


class ProjectState(Enum):
    """Project generation states."""
    CREATED = "created"
    VALIDATED = "validated"
    GENERATED = "generated"
    COMPLETED = "completed"


@dataclass
class ProjectTemplate:
    """
    Represents the complete blueprint for generating a Python project structure.
    
    Attributes:
        name: Project name (validated for Python package compatibility)
        description: Project description for README and setup files
        author: Author name for project metadata
        email: Author email for project metadata
        python_version: Minimum Python version requirement
        include_batch_files: Whether to generate Windows batch files
        template_type: Type of project template (basic, web, cli, library)
        state: Current state of the project template
    """
    name: str
    description: str = ""
    author: str = ""
    email: str = ""
    python_version: str = "3.9"
    include_batch_files: bool = True
    template_type: TemplateType = TemplateType.BASIC
    state: ProjectState = ProjectState.CREATED
    
    def __post_init__(self):
        """Post-initialization validation."""
        self.validate()
    
    def validate(self) -> bool:
        """
        Validate project template data.
        
        Returns:
            bool: True if validation passes
            
        Raises:
            ValueError: If validation fails
        """
        # Validate project name - must be valid Python identifier
        if not self.name:
            raise ValueError("Project name cannot be empty")
        
        if not self._is_valid_python_identifier(self.name):
            raise ValueError(
                f"Project name '{self.name}' must be a valid Python identifier. "
                "Use only letters, digits, and underscores. Cannot start with a digit."
            )
        
        # Validate Python version
        if not self._is_valid_python_version(self.python_version):
            raise ValueError(
                f"Python version '{self.python_version}' must be >= 3.9"
            )
        
        # Validate email if provided
        if self.email and not self._is_valid_email(self.email):
            raise ValueError(f"Email '{self.email}' is not a valid email format")
        
        # Set state to validated after successful validation
        if self.state == ProjectState.CREATED:
            self.state = ProjectState.VALIDATED
            
        return True
    
    def _is_valid_python_identifier(self, name: str) -> bool:
        """
        Check if name is a valid Python identifier.
        
        Args:
            name: Name to validate
            
        Returns:
            bool: True if valid Python identifier
        """
        # Check basic Python identifier rules
        if not name.isidentifier():
            return False
        
        # Check against Python keywords
        import keyword
        if keyword.iskeyword(name):
            return False
        
        # Additional check for common reserved names
        reserved_names = {
            'test', 'tests', 'src', 'lib', 'bin', 'doc', 'docs',
            'build', 'dist', 'egg-info', '__pycache__'
        }
        if name.lower() in reserved_names:
            return False
        
        return True
    
    def _is_valid_python_version(self, version: str) -> bool:
        """
        Check if Python version is valid and >= 3.9.
        
        Args:
            version: Version string to validate
            
        Returns:
            bool: True if valid version >= 3.9
        """
        try:
            # Parse version string (e.g., "3.9", "3.10.1")
            version_parts = version.split('.')
            if len(version_parts) < 2:
                return False
            
            major = int(version_parts[0])
            minor = int(version_parts[1])
            
            # Must be Python 3.9 or higher
            if major < 3:
                return False
            if major == 3 and minor < 9:
                return False
                
            return True
            
        except (ValueError, IndexError):
            return False
    
    def _is_valid_email(self, email: str) -> bool:
        """
        Check if email format is valid using regex.
        
        Args:
            email: Email to validate
            
        Returns:
            bool: True if valid email format
        """
        # Simple email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    def mark_generated(self):
        """Mark the template as generated."""
        if self.state == ProjectState.VALIDATED:
            self.state = ProjectState.GENERATED
    
    def mark_completed(self):
        """Mark the template as completed."""
        if self.state == ProjectState.GENERATED:
            self.state = ProjectState.COMPLETED
    
    def to_dict(self) -> dict:
        """
        Convert template to dictionary for Jinja2 templating.
        
        Returns:
            dict: Template data for rendering
        """
        return {
            'project_name': self.name,
            'project_description': self.description,
            'author_name': self.author,
            'author_email': self.email,
            'python_version': self.python_version,
            'include_batch_files': self.include_batch_files,
            'template_type': self.template_type.value,
            'state': self.state.value
        }