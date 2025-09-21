"""
ConfigurationProfile model for Python Framework Generator.
Represents different testing and quality tool configurations.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any


class ProfileType(Enum):
    """Configuration profile types."""
    BASIC = "basic"
    ADVANCED = "advanced"
    MINIMAL = "minimal"


@dataclass
class ConfigurationProfile:
    """
    Represents different testing and quality tool configurations.
    
    Attributes:
        profile_type: Type of configuration profile
        pytest_markers: Standard pytest markers to include
        coverage_settings: Code coverage configuration options
        quality_tools: Static analysis tools to configure
        pre_commit_hooks: Pre-commit hook configurations
    """
    profile_type: ProfileType = ProfileType.BASIC
    pytest_markers: List[str] = field(default_factory=list)
    coverage_settings: Dict[str, Any] = field(default_factory=dict)
    quality_tools: List[str] = field(default_factory=list)
    pre_commit_hooks: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization setup with defaults."""
        self._apply_profile_defaults()
        self.validate()
    
    def _apply_profile_defaults(self):
        """Apply default configurations based on profile type."""
        if self.profile_type == ProfileType.MINIMAL:
            self._apply_minimal_defaults()
        elif self.profile_type == ProfileType.ADVANCED:
            self._apply_advanced_defaults()
        else:  # BASIC
            self._apply_basic_defaults()
    
    def _apply_minimal_defaults(self):
        """Apply minimal profile defaults."""
        if not self.pytest_markers:
            self.pytest_markers = ['unit', 'smoke']
        
        if not self.coverage_settings:
            self.coverage_settings = {
                'fail_under': 70,
                'show_missing': True,
                'exclude_lines': ['pragma: no cover']
            }
        
        if not self.quality_tools:
            self.quality_tools = ['ruff']
        
        # No pre-commit hooks for minimal setup
        if not self.pre_commit_hooks:
            self.pre_commit_hooks = []
    
    def _apply_basic_defaults(self):
        """Apply basic profile defaults."""
        if not self.pytest_markers:
            self.pytest_markers = [
                'unit', 'integration', 'smoke', 'slow'
            ]
        
        if not self.coverage_settings:
            self.coverage_settings = {
                'fail_under': 90,
                'show_missing': True,
                'exclude_lines': [
                    'pragma: no cover',
                    'def __repr__',
                    'if self.debug:',
                    'if settings.DEBUG',
                    'raise AssertionError',
                    'raise NotImplementedError'
                ],
                'omit': [
                    '*/tests/*',
                    '*/test_*',
                    'setup.py'
                ]
            }
        
        if not self.quality_tools:
            self.quality_tools = ['ruff', 'black']
        
        if not self.pre_commit_hooks:
            self.pre_commit_hooks = ['ruff-check', 'black']
    
    def _apply_advanced_defaults(self):
        """Apply advanced profile defaults."""
        if not self.pytest_markers:
            self.pytest_markers = [
                'unit', 'integration', 'contract', 'performance',
                'smoke', 'slow', 'security', 'regression'
            ]
        
        if not self.coverage_settings:
            self.coverage_settings = {
                'fail_under': 95,
                'show_missing': True,
                'skip_covered': False,
                'exclude_lines': [
                    'pragma: no cover',
                    'def __repr__',
                    'if self.debug:',
                    'if settings.DEBUG',
                    'raise AssertionError',
                    'raise NotImplementedError',
                    'if 0:',
                    'if __name__ == .__main__.:'
                ],
                'omit': [
                    '*/tests/*',
                    '*/test_*',
                    'setup.py',
                    '*/migrations/*'
                ],
                'precision': 2
            }
        
        if not self.quality_tools:
            self.quality_tools = [
                'ruff', 'black', 'mypy', 'bandit', 'safety'
            ]
        
        if not self.pre_commit_hooks:
            self.pre_commit_hooks = [
                'ruff-check', 'ruff-format', 'black', 'mypy',
                'bandit', 'safety', 'check-yaml', 'check-toml'
            ]
    
    def validate(self) -> bool:
        """
        Validate configuration profile.
        
        Returns:
            bool: True if validation passes
            
        Raises:
            ValueError: If validation fails
        """
        # Validate pytest markers
        for marker in self.pytest_markers:
            if not marker.isidentifier():
                raise ValueError(f"Invalid pytest marker: '{marker}'")
        
        # Validate coverage settings
        if 'fail_under' in self.coverage_settings:
            fail_under = self.coverage_settings['fail_under']
            if not isinstance(fail_under, (int, float)) or not 0 <= fail_under <= 100:
                raise ValueError("Coverage fail_under must be between 0 and 100")
        
        # Validate quality tools
        valid_tools = {
            'ruff', 'black', 'mypy', 'flake8', 'pylint', 
            'bandit', 'safety', 'isort', 'autopep8'
        }
        for tool in self.quality_tools:
            if tool not in valid_tools:
                raise ValueError(f"Unsupported quality tool: '{tool}'")
        
        return True
    
    def get_pytest_config(self) -> Dict[str, Any]:
        """
        Get pytest configuration.
        
        Returns:
            dict: Pytest configuration
        """
        markers = []
        marker_descriptions = {
            'unit': 'marks tests as unit tests',
            'integration': 'marks tests as integration tests',
            'contract': 'marks tests as contract tests',
            'performance': 'marks tests as performance tests',
            'smoke': 'marks tests as smoke tests for basic functionality',
            'slow': 'marks tests as slow (deselect with \'-m "not slow"\')',
            'security': 'marks tests as security tests',
            'regression': 'marks tests as regression tests'
        }
        
        for marker in self.pytest_markers:
            description = marker_descriptions.get(marker, f'marks tests as {marker}')
            markers.append(f'{marker}: {description}')
        
        return {
            'testpaths': ['tests'],
            'python_files': ['test_*.py'],
            'python_classes': ['Test*'],
            'python_functions': ['test_*'],
            'addopts': [
                '--strict-markers',
                '--strict-config',
                '--cov=src',
                '--cov-report=term-missing',
                '--cov-report=html',
                f'--cov-fail-under={self.coverage_settings.get("fail_under", 90)}',
                '-v'
            ],
            'markers': markers
        }
    
    def get_coverage_config(self) -> Dict[str, Any]:
        """
        Get coverage configuration.
        
        Returns:
            dict: Coverage configuration
        """
        return {
            'run': {
                'source': ['src'],
                'omit': self.coverage_settings.get('omit', [])
            },
            'report': {
                'show_missing': self.coverage_settings.get('show_missing', True),
                'skip_covered': self.coverage_settings.get('skip_covered', False),
                'exclude_lines': self.coverage_settings.get('exclude_lines', []),
                'precision': self.coverage_settings.get('precision', 1)
            },
            'html': {
                'directory': 'htmlcov'
            }
        }
    
    def get_quality_tools_config(self) -> Dict[str, Any]:
        """
        Get quality tools configuration.
        
        Returns:
            dict: Quality tools configuration
        """
        config = {}
        
        if 'ruff' in self.quality_tools:
            config['ruff'] = {
                'target-version': 'py39',
                'line-length': 100,
                'select': ['E', 'W', 'F', 'I', 'B', 'C4', 'UP'],
                'ignore': ['E501', 'B008']
            }
        
        if 'black' in self.quality_tools:
            config['black'] = {
                'target-version': ['py39'],
                'line-length': 100,
                'include': '\\.pyi?$'
            }
        
        if 'mypy' in self.quality_tools:
            config['mypy'] = {
                'python_version': '3.9',
                'warn_return_any': True,
                'warn_unused_configs': True,
                'disallow_untyped_defs': True
            }
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration profile to dictionary.
        
        Returns:
            dict: Configuration profile data
        """
        return {
            'profile_type': self.profile_type.value,
            'pytest_markers': self.pytest_markers,
            'coverage_settings': self.coverage_settings,
            'quality_tools': self.quality_tools,
            'pre_commit_hooks': self.pre_commit_hooks,
            'pytest_config': self.get_pytest_config(),
            'coverage_config': self.get_coverage_config(),
            'quality_tools_config': self.get_quality_tools_config()
        }