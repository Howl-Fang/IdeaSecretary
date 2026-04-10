from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Idea, IdeaBase
from services.openai_service import OpenAIClient
from services.backup_service import BackupService
import json

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/organize', methods=['POST'])
@jwt_required()
def organize_idea():
    """Get AI suggestions for organizing an idea"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not user.openai_api_key:
        return jsonify({'error': 'OpenAI API not configured'}), 400
    
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Missing title or content'}), 400
    
    try:
        client = OpenAIClient(
            api_key=user.openai_api_key,
            api_url=user.openai_api_url or 'https://api.openai.com/v1',
            model=user.openai_model or 'gpt-3.5-turbo'
        )
        
        suggestion = client.organize_idea(
            content=data['content'],
            title=data['title']
        )
        
        if suggestion:
            return jsonify({'suggestion': suggestion}), 200
        else:
            return jsonify({'error': 'Failed to get AI suggestion'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/inspire', methods=['POST'])
@jwt_required()
def get_inspiration():
    """Get AI-generated inspiration based on existing ideas"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not user.openai_api_key:
        return jsonify({'error': 'OpenAI API not configured'}), 400
    
    data = request.get_json()
    base_id = data.get('base_id')
    
    if not base_id:
        return jsonify({'error': 'Missing base_id'}), 400
    
    base = IdeaBase.query.filter_by(id=base_id, user_id=user_id).first()
    
    if not base:
        return jsonify({'error': 'Idea base not found'}), 404
    
    try:
        # Collect existing ideas
        existing_ideas = []
        for idea in base.ideas:
            existing_ideas.append(f"{idea.title}: {idea.content[:100]}")
        
        if not existing_ideas:
            return jsonify({'error': 'No existing ideas to base inspiration on'}), 400
        
        client = OpenAIClient(
            api_key=user.openai_api_key,
            api_url=user.openai_api_url or 'https://api.openai.com/v1',
            model=user.openai_model or 'gpt-3.5-turbo'
        )
        
        inspiration = client.generate_inspiration(existing_ideas)
        
        if inspiration:
            return jsonify({'inspiration': inspiration}), 200
        else:
            return jsonify({'error': 'Failed to generate inspiration'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/summarize', methods=['POST'])
@jwt_required()
def summarize_ideas():
    """Summarize multiple ideas"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not user.openai_api_key:
        return jsonify({'error': 'OpenAI API not configured'}), 400
    
    data = request.get_json()
    
    if not data or 'idea_ids' not in data:
        return jsonify({'error': 'Missing idea_ids'}), 400
    
    idea_ids = data['idea_ids']
    
    try:
        # Get ideas
        ideas_data = []
        for idea_id in idea_ids:
            idea = db.session.query(Idea).join(IdeaBase).filter(
                Idea.id == idea_id,
                IdeaBase.user_id == user_id
            ).first()
            
            if idea:
                ideas_data.append(f"{idea.title}: {idea.content}")
        
        if not ideas_data:
            return jsonify({'error': 'No ideas found'}), 400
        
        client = OpenAIClient(
            api_key=user.openai_api_key,
            api_url=user.openai_api_url or 'https://api.openai.com/v1',
            model=user.openai_model or 'gpt-3.5-turbo'
        )
        
        summary = client.summarize_ideas(ideas_data)
        
        if summary:
            return jsonify({'summary': summary}), 200
        else:
            return jsonify({'error': 'Failed to summarize'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
