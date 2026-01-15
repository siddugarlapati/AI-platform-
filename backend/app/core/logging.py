"""
Logging Configuration
"""

import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging():
    """Setup application logging"""
    logger = logging.getLogger("aiza")
    logger.setLevel(logging.INFO)
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
