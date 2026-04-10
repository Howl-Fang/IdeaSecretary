from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.auth_service import create_user, authenticate_user
from models import db, User, IdeaBase

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    user, error = create_user(username, email, password)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Create default idea base
    default_base = IdeaBase(
        user_id=user.id,
        name='My Knowledge Base',
        description='Default knowledge base',
        is_default=True
    )
    db.session.add(default_base)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'access_token': access_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = authenticate_user(data.get('username'), data.get('password'))
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'access_token': access_token
    }), 200

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify JWT token"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    }), 200
