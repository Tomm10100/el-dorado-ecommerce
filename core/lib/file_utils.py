"""
File utilities shared across Antigravity modules
"""

import re
from pathlib import Path
from typing import Union


def create_slug(text: str, max_length: int = 50) -> str:
    """
    Create a URL-friendly slug from text
    
    Args:
        text: Input text to slugify
        max_length: Maximum slug length
    
    Returns:
        URL-friendly slug
    """
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug[:max_length]


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if needed
    
    Args:
        path: Directory path
    
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_size_human(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Human-readable size (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
