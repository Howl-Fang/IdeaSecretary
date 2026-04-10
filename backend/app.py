import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
from config import config
from datetime import datetime

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    config_obj = config.get(config_name, config['development'])
    app.config.from_object(config_obj)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.ideas import ideas_bp
    from routes.media import media_bp
    from routes.user import user_bp
    from routes.search import search_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(ideas_bp, url_prefix='/api/ideas')
    app.register_blueprint(media_bp, url_prefix='/api/media')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
