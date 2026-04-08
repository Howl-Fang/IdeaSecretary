from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

bp = Blueprint('account', __name__, url_prefix='/api/account')

@bp.route('/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user profile"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'language': user.language,
        'theme': user.theme,
        'created_at': user.created_at.isoformat()
    }), 200

@bp.route('/profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    """Update user profile"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'language' in data:
        user.language = data['language']
    if 'theme' in data:
        user.theme = data['theme']
    if 'email' in data:
        # Check if email is unique
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user.id:
            return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify({'message': 'Profile updated'}), 200

@bp.route('/openai-config/<user_id>', methods=['GET'])
def get_openai_config(user_id):
    """Get OpenAI configuration"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'has_api_key': bool(user.openai_api_key),
        'api_base': user.openai_api_base or 'https://api.openai.com/v1'
    }), 200

@bp.route('/openai-config/<user_id>', methods=['PUT'])
def set_openai_config(user_id):
    """Set OpenAI configuration"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'api_key' in data:
        user.openai_api_key = data['api_key']
    if 'api_base' in data:
        user.openai_api_base = data['api_base']
    
    db.session.commit()
    
    return jsonify({'message': 'OpenAI configuration updated'}), 200
