# /backend/config.py
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'a-super-secret-jwt-key'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # For easy local setup, you can use SQLite:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///ajali_dev.db'
    # For PostgreSQL:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/ajali_db'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    # Use an in-memory SQLite database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'