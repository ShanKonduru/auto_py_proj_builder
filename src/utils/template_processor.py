"""
Template processing utilities for Python Framework Generator.
Handles template rendering, context preparation, and file processing.
"""
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Environment, BaseLoader, Template, TemplateError


class TemplateProcessor:
    """
    Processes templates with context data and handles template operations.
    
    Provides template rendering, variable substitution, and content processing
    for project generation.
    """
    
    def __init__(self):
        """Initialize template processor with Jinja2 environment."""
        self.env = Environment(
            loader=BaseLoader(),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        
        # Add custom filters
        self.env.filters['snake_case'] = self.to_snake_case
        self.env.filters['pascal_case'] = self.to_pascal_case
        self.env.filters['kebab_case'] = self.to_kebab_case
        self.env.filters['upper_case'] = str.upper
        self.env.filters['lower_case'] = str.lower
        self.env.filters['title_case'] = str.title
    
    def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """
        Render a template string with given context.
        
        Args:
            template_string: Template content as string
            context: Context variables for rendering
            
        Returns:
            str: Rendered content
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template = self.env.from_string(template_string)
            return template.render(**context)
        except TemplateError as e:
            raise TemplateError(f"Template rendering failed: {str(e)}")
    
    def render_file_path(self, file_path: str, context: Dict[str, Any]) -> str:
        """
        Render a file path template with context variables.
        
        Useful for dynamic file paths like "{{project_name}}/src/main.py"
        
        Args:
            file_path: File path template
            context: Context variables
            
        Returns:
            str: Rendered file path
        """
        try:
            # Use a simpler template for file paths to avoid issues with path separators
            template_str = file_path
            
            # Replace template variables in the path
            for key, value in context.items():
                template_str = template_str.replace(f"{{{{{key}}}}}", str(value))
            
            return template_str
        except Exception as e:
            raise TemplateError(f"File path rendering failed: {str(e)}")
    
    def process_template_content(self, content: str, context: Dict[str, Any]) -> str:
        """
        Process template content with advanced features.
        
        Handles conditional blocks, loops, and custom processing.
        
        Args:
            content: Template content
            context: Render context
            
        Returns:
            str: Processed content
        """
        # Pre-process conditional blocks
        content = self._process_conditional_blocks(content, context)
        
        # Render with Jinja2
        rendered = self.render_string(content, context)
        
        # Post-process: clean up extra whitespace
        rendered = self._clean_whitespace(rendered)
        
        return rendered
    
    def _process_conditional_blocks(self, content: str, context: Dict[str, Any]) -> str:
        """
        Process custom conditional blocks.
        
        Supports syntax like:
        #if include_tests
        # Test-related content
        #endif
        """
        lines = content.split('\n')
        processed_lines = []
        condition_stack = []
        skip_until = None
        
        for line in lines:
            stripped = line.strip()
            
            # Handle #if conditions
            if stripped.startswith('#if '):
                condition = stripped[4:].strip()
                is_true = self._evaluate_condition(condition, context)
                condition_stack.append(is_true)
                
                if not is_true and skip_until is None:
                    skip_until = len(condition_stack)
                continue
            
            # Handle #endif
            elif stripped == '#endif':
                if condition_stack:
                    was_true = condition_stack.pop()
                    if skip_until == len(condition_stack) + 1:
                        skip_until = None
                continue
            
            # Handle #else
            elif stripped == '#else':
                if condition_stack:
                    condition_stack[-1] = not condition_stack[-1]
                    if skip_until == len(condition_stack):
                        skip_until = None
                    elif condition_stack[-1] is False and skip_until is None:
                        skip_until = len(condition_stack)
                continue
            
            # Add line if not skipping
            if skip_until is None:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """
        Evaluate a condition string against context.
        
        Supports:
        - Variable names: "include_tests"
        - Equality: "template_type == 'cli'"
        - Inequality: "python_version != '3.8'"
        """
        condition = condition.strip()
        
        # Simple variable check
        if condition in context:
            return bool(context[condition])
        
        # Equality check
        if ' == ' in condition:
            left, right = condition.split(' == ', 1)
            left_val = context.get(left.strip())
            right_val = right.strip().strip("'\"")
            return str(left_val) == right_val
        
        # Inequality check
        if ' != ' in condition:
            left, right = condition.split(' != ', 1)
            left_val = context.get(left.strip())
            right_val = right.strip().strip("'\"")
            return str(left_val) != right_val
        
        # Default to False for unknown conditions
        return False
    
    def _clean_whitespace(self, content: str) -> str:
        """Clean up extra whitespace from rendered content."""
        # Remove trailing whitespace from each line
        lines = [line.rstrip() for line in content.split('\n')]
        
        # Remove excessive blank lines (more than 2 consecutive)
        cleaned_lines = []
        blank_count = 0
        
        for line in lines:
            if line.strip() == '':
                blank_count += 1
                if blank_count <= 2:
                    cleaned_lines.append(line)
            else:
                blank_count = 0
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def extract_variables(self, template_content: str) -> List[str]:
        """
        Extract variable names from template content.
        
        Args:
            template_content: Template content
            
        Returns:
            List[str]: List of variable names found
        """
        # Find Jinja2 variables {{ variable_name }}
        jinja_vars = re.findall(r'\{\{\s*(\w+)\s*\}\}', template_content)
        
        # Find custom conditional variables #if variable_name
        cond_vars = re.findall(r'#if\s+(\w+)', template_content)
        
        # Combine and deduplicate
        all_vars = list(set(jinja_vars + cond_vars))
        return sorted(all_vars)
    
    def validate_template(self, template_content: str) -> List[str]:
        """
        Validate template syntax and return any errors.
        
        Args:
            template_content: Template content to validate
            
        Returns:
            List[str]: List of validation error messages
        """
        errors = []
        
        try:
            # Try to parse as Jinja2 template
            self.env.from_string(template_content)
        except TemplateError as e:
            errors.append(f"Jinja2 syntax error: {str(e)}")
        
        # Check for unmatched conditional blocks
        if_count = template_content.count('#if ')
        endif_count = template_content.count('#endif')
        
        if if_count != endif_count:
            errors.append(f"Unmatched conditional blocks: {if_count} #if, {endif_count} #endif")
        
        return errors
    
    def create_template_context(self, **kwargs) -> Dict[str, Any]:
        """
        Create a template context with common variables and utilities.
        
        Args:
            **kwargs: Additional context variables
            
        Returns:
            Dict[str, Any]: Template context
        """
        import datetime
        import platform
        
        context = {
            # Time and date
            'current_year': datetime.datetime.now().year,
            'current_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'current_datetime': datetime.datetime.now().isoformat(),
            
            # System information
            'platform': platform.system().lower(),
            'is_windows': platform.system().lower() == 'windows',
            'is_linux': platform.system().lower() == 'linux',
            'is_macos': platform.system().lower() == 'darwin',
            
            # Generator information
            'generator_name': 'Python Framework Generator',
            'generator_version': '0.1.0',
        }
        
        # Add user-provided variables
        context.update(kwargs)
        
        return context
    
    @staticmethod
    def to_snake_case(text: str) -> str:
        """Convert text to snake_case."""
        # Replace spaces and hyphens with underscores
        text = re.sub(r'[-\s]+', '_', text)
        
        # Insert underscores before capital letters
        text = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
        
        return text.lower()
    
    @staticmethod
    def to_pascal_case(text: str) -> str:
        """Convert text to PascalCase."""
        # Split on underscores, hyphens, and spaces
        words = re.split(r'[-_\s]+', text)
        
        # Capitalize each word
        return ''.join(word.capitalize() for word in words if word)
    
    @staticmethod
    def to_kebab_case(text: str) -> str:
        """Convert text to kebab-case."""
        # Replace spaces and underscores with hyphens
        text = re.sub(r'[_\s]+', '-', text)
        
        # Insert hyphens before capital letters
        text = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', text)
        
        return text.lower()
    
    def render_template_file(self, template_path: Path, output_path: Path, 
                           context: Dict[str, Any]) -> bool:
        """
        Render a template file to an output file.
        
        Args:
            template_path: Path to template file
            output_path: Path to output file
            context: Template context
            
        Returns:
            bool: True if successful
            
        Raises:
            TemplateError: If rendering fails
        """
        try:
            # Read template content
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Render content
            rendered_content = self.process_template_content(template_content, context)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write rendered content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered_content)
            
            return True
            
        except Exception as e:
            raise TemplateError(f"Failed to render template {template_path}: {str(e)}")
    
    def batch_render(self, template_files: List[Path], output_dir: Path,
                    context: Dict[str, Any]) -> List[Path]:
        """
        Render multiple template files to an output directory.
        
        Args:
            template_files: List of template file paths
            output_dir: Output directory
            context: Template context
            
        Returns:
            List[Path]: List of generated file paths
        """
        generated_files = []
        
        for template_path in template_files:
            # Determine output file path
            relative_path = template_path.name
            if relative_path.endswith('.template'):
                relative_path = relative_path[:-9]  # Remove .template extension
            
            output_path = output_dir / relative_path
            
            try:
                self.render_template_file(template_path, output_path, context)
                generated_files.append(output_path)
            except TemplateError:
                # Skip files that fail to render
                continue
        
        return generated_files