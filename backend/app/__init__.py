from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import auth, ideas, ai, account
    app.register_blueprint(auth.bp)
    app.register_blueprint(ideas.bp)
    app.register_blueprint(ai.bp)
    app.register_blueprint(account.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
