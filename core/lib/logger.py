"""
Consistent logging across Antigravity platform
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def get_logger(module_name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Get a configured logger for a module
    
    Args:
        module_name: Name of the module (e.g., "content-creation")
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(f"antigravity.{module_name}")
    
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level))
        
        # File handler
        log_dir = Path(".logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f"{module_name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Format
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
    
    return logger
