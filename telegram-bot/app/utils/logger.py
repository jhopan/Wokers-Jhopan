"""
Logging configuration
"""

import logging
import sys
from app.config import Config


def setup_logger(name: str = None) -> logging.Logger:
    """Setup and configure logger"""
    
    # Create logger
    logger = logging.getLogger(name or __name__)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
