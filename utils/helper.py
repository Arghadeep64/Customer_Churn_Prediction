"""
Helper Functions Module
Utility functions used across the application
"""

import logging
from utils.config import LOG_LEVEL, LOG_FILE
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_info(message):
    """Log info message"""
    logger.info(message)

def log_error(message):
    """Log error message"""
    logger.error(message)

def log_warning(message):
    """Log warning message"""
    logger.warning(message)

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def format_percentage(value):
    """Format value as percentage"""
    return f"{value * 100:.2f}%"

def format_currency(value):
    """Format value as currency"""
    return f"${value:.2f}"

def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def save_json(data, filepath):
    """Save data to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        log_info(f"Data saved to {filepath}")
    except Exception as e:
        log_error(f"Error saving JSON: {str(e)}")

def load_json(filepath):
    """Load data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        log_error(f"Error loading JSON: {str(e)}")
        return None
