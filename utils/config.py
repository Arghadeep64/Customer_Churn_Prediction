"""
Configuration Module
Centralized configuration for the application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///churn_prediction.db')

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
DEBUG = os.getenv('DEBUG', True)

# Model Configuration
MODEL_PATH = os.getenv('MODEL_PATH', 'models/churn_model.pkl')
DATA_PATH = os.getenv('DATA_PATH', 'dataset/customer_churn.csv')

# Dashboard Configuration
DASH_PORT = int(os.getenv('DASH_PORT', 8050))
DASH_DEBUG = os.getenv('DASH_DEBUG', True)

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'app.log')

# Feature Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
MODEL_TYPE = os.getenv('MODEL_TYPE', 'random_forest')

# Threshold Configuration
CHURN_RISK_THRESHOLD = 0.5
HIGH_RISK_THRESHOLD = 0.7
MEDIUM_RISK_THRESHOLD = 0.3
