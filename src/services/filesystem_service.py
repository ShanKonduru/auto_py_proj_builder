"""
FileSystemService for Python Framework Generator.
Handles all file system operations with error handling and validation.
"""
import os
import shutil
import stat
from pathlib import Path
from typing import Optional


class FileSystemService:
    """
    Service for handling file system operations.
    
    Provides safe file and directory operations with proper error handling.
    """
    
    def __init__(self):
        """Initialize filesystem service."""
        pass
    
    def create_directory(self, path: Path, exist_ok: bool = True) -> bool:
        """
        Create a directory and all parent directories.
        
        Args:
            path: Directory path to create
            exist_ok: Don't raise error if directory exists
            
        Returns:
            bool: True if successful
            
        Raises:
            OSError: If directory creation fails
        """
        try:
            path.mkdir(parents=True, exist_ok=exist_ok)
            return True
        except OSError as e:
            raise OSError(f"Failed to create directory {path}: {str(e)}")
    
    def remove_directory(self, path: Path, ignore_errors: bool = True) -> bool:
        """
        Remove a directory and all its contents.
        
        Args:
            path: Directory path to remove
            ignore_errors: Don't raise error if removal fails
            
        Returns:
            bool: True if successful
            
        Raises:
            OSError: If removal fails and ignore_errors is False
        """
        try:
            if path.exists():
                shutil.rmtree(path, ignore_errors=ignore_errors)
            return True
        except OSError as e:
            if not ignore_errors:
                raise OSError(f"Failed to remove directory {path}: {str(e)}")
            return False
    
    def write_file(self, path: Path, content: str, encoding: str = 'utf-8') -> bool:
        """
        Write content to a file.
        
        Args:
            path: File path to write
            content: Content to write
            encoding: File encoding
            
        Returns:
            bool: True if successful
            
        Raises:
            OSError: If file write fails
        """
        try:
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except OSError as e:
            raise OSError(f"Failed to write file {path}: {str(e)}")
    
    def read_file(self, path: Path, encoding: str = 'utf-8') -> str:
        """
        Read content from a file.
        
        Args:
            path: File path to read
            encoding: File encoding
            
        Returns:
            str: File content
            
        Raises:
            OSError: If file read fails
        """
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.read()
        except OSError as e:
            raise OSError(f"Failed to read file {path}: {str(e)}")
    
    def copy_file(self, src: Path, dst: Path) -> bool:
        """
        Copy a file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            bool: True if successful
            
        Raises:
            OSError: If copy fails
        """
        try:
            shutil.copy2(src, dst)
            return True
        except OSError as e:
            raise OSError(f"Failed to copy file {src} to {dst}: {str(e)}")
    
    def move_file(self, src: Path, dst: Path) -> bool:
        """
        Move a file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            bool: True if successful
            
        Raises:
            OSError: If move fails
        """
        try:
            shutil.move(str(src), str(dst))
            return True
        except OSError as e:
            raise OSError(f"Failed to move file {src} to {dst}: {str(e)}")
    
    def make_executable(self, path: Path) -> bool:
        """
        Make a file executable.
        
        Args:
            path: File path to make executable
            
        Returns:
            bool: True if successful
            
        Raises:
            OSError: If permission change fails
        """
        try:
            # On Windows, this is mostly a no-op since .bat/.cmd files are executable by extension
            if os.name == 'nt':
                return True
            
            # On Unix-like systems, add execute permission
            current_mode = path.stat().st_mode
            new_mode = current_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
            path.chmod(new_mode)
            return True
        except OSError as e:
            raise OSError(f"Failed to make file {path} executable: {str(e)}")
    
    def file_exists(self, path: Path) -> bool:
        """
        Check if a file exists.
        
        Args:
            path: File path to check
            
        Returns:
            bool: True if file exists
        """
        return path.exists() and path.is_file()
    
    def directory_exists(self, path: Path) -> bool:
        """
        Check if a directory exists.
        
        Args:
            path: Directory path to check
            
        Returns:
            bool: True if directory exists
        """
        return path.exists() and path.is_dir()
    
    def get_file_size(self, path: Path) -> int:
        """
        Get file size in bytes.
        
        Args:
            path: File path
            
        Returns:
            int: File size in bytes
            
        Raises:
            OSError: If file doesn't exist or can't be accessed
        """
        try:
            return path.stat().st_size
        except OSError as e:
            raise OSError(f"Failed to get size of file {path}: {str(e)}")
    
    def list_directory_contents(self, path: Path, pattern: str = "*") -> list:
        """
        List contents of a directory.
        
        Args:
            path: Directory path
            pattern: Glob pattern to match
            
        Returns:
            list: List of Path objects
            
        Raises:
            OSError: If directory doesn't exist or can't be accessed
        """
        try:
            if not self.directory_exists(path):
                raise OSError(f"Directory {path} does not exist")
            
            return list(path.glob(pattern))
        except OSError as e:
            raise OSError(f"Failed to list directory {path}: {str(e)}")
    
    def create_symlink(self, target: Path, link: Path) -> bool:
        """
        Create a symbolic link.
        
        Args:
            target: Target path
            link: Link path
            
        Returns:
            bool: True if successful
            
        Raises:
            OSError: If symlink creation fails
        """
        try:
            link.symlink_to(target)
            return True
        except OSError as e:
            raise OSError(f"Failed to create symlink {link} -> {target}: {str(e)}")
    
    def is_empty_directory(self, path: Path) -> bool:
        """
        Check if a directory is empty.
        
        Args:
            path: Directory path
            
        Returns:
            bool: True if directory is empty
            
        Raises:
            OSError: If directory doesn't exist or can't be accessed
        """
        try:
            if not self.directory_exists(path):
                raise OSError(f"Directory {path} does not exist")
            
            return len(list(path.iterdir())) == 0
        except OSError as e:
            raise OSError(f"Failed to check if directory {path} is empty: {str(e)}")
    
    def ensure_parent_directory(self, file_path: Path) -> bool:
        """
        Ensure that the parent directory of a file exists.
        
        Args:
            file_path: File path whose parent should exist
            
        Returns:
            bool: True if successful
        """
        parent = file_path.parent
        if not parent.exists():
            return self.create_directory(parent)
        return True
    
    def get_absolute_path(self, path: Path) -> Path:
        """
        Get absolute path, resolving any relative components.
        
        Args:
            path: Path to resolve
            
        Returns:
            Path: Absolute path
        """
        return path.resolve()
    
    def safe_filename(self, filename: str) -> str:
        """
        Convert a string to a safe filename by removing invalid characters.
        
        Args:
            filename: Original filename
            
        Returns:
            str: Safe filename
        """
        # Characters that are generally invalid in filenames
        invalid_chars = '<>:"/\\|?*'
        safe_name = filename
        
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')
        
        # Remove any leading/trailing spaces or dots
        safe_name = safe_name.strip(' .')
        
        # Ensure it's not empty
        if not safe_name:
            safe_name = 'unnamed'
        
        return safe_name