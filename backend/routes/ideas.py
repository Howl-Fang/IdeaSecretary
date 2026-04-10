from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Idea, IdeaBase, SearchIndex, User
from services.backup_service import BackupService
import json
from datetime import datetime

ideas_bp = Blueprint('ideas', __name__)

@ideas_bp.route('/bases', methods=['GET'])
@jwt_required()
def get_idea_bases():
    """Get all idea bases for user"""
    user_id = get_jwt_identity()
    bases = IdeaBase.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'bases': [{
            'id': base.id,
            'name': base.name,
            'description': base.description,
            'is_default': base.is_default,
            'idea_count': base.idea_count,
            'total_word_count': base.total_word_count,
            'created_at': base.created_at.isoformat()
        } for base in bases]
    }), 200

@ideas_bp.route('/<base_id>', methods=['GET'])
@jwt_required()
def get_idea_tree(base_id):
    """Get idea tree for a base"""
    user_id = get_jwt_identity()
    base = IdeaBase.query.filter_by(id=base_id, user_id=user_id).first()
    
    if not base:
        return jsonify({'error': 'Idea base not found'}), 404
    
    root_ideas = Idea.query.filter_by(idea_base_id=base_id, parent_id=None).order_by(Idea.order).all()
    
    def build_tree(idea):
        return {
            'id': idea.id,
            'title': idea.title,
            'content': idea.content,
            'ai_thought': idea.ai_thought,
            'tags': json.loads(idea.tags) if idea.tags else [],
            'content_type': idea.content_type,
            'created_at': idea.created_at.isoformat(),
            'children': [build_tree(child) for child in sorted(idea.children, key=lambda x: x.order)]
        }
    
    return jsonify({
        'ideas': [build_tree(idea) for idea in root_ideas]
    }), 200

@ideas_bp.route('/<base_id>/create', methods=['POST'])
@jwt_required()
def create_idea(base_id):
    """Create new idea"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    base = IdeaBase.query.filter_by(id=base_id, user_id=user_id).first()
    
    if not base:
        return jsonify({'error': 'Idea base not found'}), 404
    
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Missing title or content'}), 400
    
    idea = Idea(
        idea_base_id=base_id,
        parent_id=data.get('parent_id'),
        title=data.get('title'),
        content=data.get('content'),
        ai_thought=data.get('ai_thought'),
        tags=json.dumps(data.get('tags', [])),
        content_type=data.get('content_type', 'text'),
        media_ids=json.dumps(data.get('media_ids', [])),
        order=data.get('order', 0)
    )
    
    db.session.add(idea)
    base.idea_count += 1
    base.total_word_count += len(data.get('content', '').split())
    
    # Add to search index
    search_entry = SearchIndex(
        idea_id=idea.id,
        search_text=f"{idea.title} {idea.content}"
    )
    db.session.add(search_entry)
    
    db.session.commit()
    
    # Increment operation count and check for backup
    BackupService.increment_operation_count(user)
    
    return jsonify({
        'id': idea.id,
        'title': idea.title,
        'created_at': idea.created_at.isoformat()
    }), 201

@ideas_bp.route('/<idea_id>', methods=['GET'])
@jwt_required()
def get_idea(idea_id):
    """Get single idea"""
    user_id = get_jwt_identity()
    idea = db.session.query(Idea).join(IdeaBase).filter(
        Idea.id == idea_id,
        IdeaBase.user_id == user_id
    ).first()
    
    if not idea:
        return jsonify({'error': 'Idea not found'}), 404
    
    return jsonify({
        'id': idea.id,
        'title': idea.title,
        'content': idea.content,
        'ai_thought': idea.ai_thought,
        'tags': json.loads(idea.tags) if idea.tags else [],
        'content_type': idea.content_type,
        'media_ids': json.loads(idea.media_ids) if idea.media_ids else [],
        'created_at': idea.created_at.isoformat(),
        'updated_at': idea.updated_at.isoformat()
    }), 200

@ideas_bp.route('/<idea_id>', methods=['PUT'])
@jwt_required()
def update_idea(idea_id):
    """Update idea"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    idea = db.session.query(Idea).join(IdeaBase).filter(
        Idea.id == idea_id,
        IdeaBase.user_id == user_id
    ).first()
    
    if not idea:
        return jsonify({'error': 'Idea not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        idea.title = data['title']
    if 'content' in data:
        idea.content = data['content']
    if 'ai_thought' in data:
        idea.ai_thought = data['ai_thought']
    if 'tags' in data:
        idea.tags = json.dumps(data['tags'])
    
    idea.updated_at = datetime.utcnow()
    
    # Update search index
    search_entry = SearchIndex.query.filter_by(idea_id=idea_id).first()
    if search_entry:
        search_entry.search_text = f"{idea.title} {idea.content}"
    
    db.session.commit()
    
    # Increment operation count and check for backup
    BackupService.increment_operation_count(user)
    
    return jsonify({
        'id': idea.id,
        'updated_at': idea.updated_at.isoformat()
    }), 200

@ideas_bp.route('/<idea_id>', methods=['DELETE'])
@jwt_required()
def delete_idea(idea_id):
    """Delete idea"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    idea = db.session.query(Idea).join(IdeaBase).filter(
        Idea.id == idea_id,
        IdeaBase.user_id == user_id
    ).first()
    
    if not idea:
        return jsonify({'error': 'Idea not found'}), 404
    
    base = idea.idea_base
    word_count = len(idea.content.split())
    
    db.session.delete(idea)
    base.idea_count -= 1
    base.total_word_count -= word_count
    
    db.session.commit()
    
    # Increment operation count and check for backup
    BackupService.increment_operation_count(user)
    
    return jsonify({'message': 'Idea deleted'}), 200
