from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, IdeaBase

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'language': user.language,
        'dark_mode': user.dark_mode,
        'openai_configured': bool(user.openai_api_key),
        'created_at': user.created_at.isoformat()
    }), 200

@user_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    """Update user settings"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'language' in data:
        user.language = data['language']
    if 'dark_mode' in data:
        user.dark_mode = data['dark_mode']
    
    db.session.commit()
    
    return jsonify({'message': 'Settings updated'}), 200

@user_bp.route('/openai-config', methods=['POST'])
@jwt_required()
def set_openai_config():
    """Set OpenAI API configuration"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'api_key' not in data or 'api_url' not in data or 'model' not in data:
        return jsonify({'error': 'Missing api_key, api_url, or model'}), 400
    
    user.openai_api_key = data['api_key']
    user.openai_api_url = data['api_url']
    user.openai_model = data['model']
    
    db.session.commit()
    
    return jsonify({'message': 'OpenAI config updated'}), 200

@user_bp.route('/openai-config', methods=['GET'])
@jwt_required()
def get_openai_config():
    """Get OpenAI API configuration (without key)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'api_url': user.openai_api_url or 'https://api.openai.com/v1',
        'model': user.openai_model or 'gpt-3.5-turbo',
        'configured': bool(user.openai_api_key)
    }), 200

@user_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """Get user statistics"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    bases = IdeaBase.query.filter_by(user_id=user_id).all()
    total_ideas = sum(base.idea_count for base in bases)
    total_words = sum(base.total_word_count for base in bases)
    
    return jsonify({
        'total_idea_bases': len(bases),
        'total_ideas': total_ideas,
        'total_word_count': total_words,
        'operation_count': user.operation_count
    }), 200
