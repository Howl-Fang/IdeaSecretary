import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:////Users/lihaofang/Documents/IdeaSecretary/data/idea_secretary.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # AI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
    
    # Media Configuration
    MEDIA_FOLDER = os.getenv('MEDIA_FOLDER', '/Users/lihaofang/Documents/IdeaSecretary/data/media')
    MEDIA_TRASH_FOLDER = os.getenv('MEDIA_TRASH_FOLDER', '/Users/lihaofang/Documents/IdeaSecretary/data/media_trash')
    BACKUP_FOLDER = os.getenv('BACKUP_FOLDER', '/Users/lihaofang/Documents/IdeaSecretary/data/backups')
    
    # Backup Configuration
    BACKUP_INTERVAL = 100  # Number of operations before backup
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
