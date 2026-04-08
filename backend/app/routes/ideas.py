from flask import Blueprint, request, jsonify
from app import db
from app.models import Idea, IdeaLibrary

bp = Blueprint('ideas', __name__, url_prefix='/api/ideas')

@bp.route('/libraries', methods=['GET'])
def get_libraries():
    """Get all idea libraries for the current user"""
    # TODO: Implement user authentication
    user_id = request.args.get('user_id')
    
    libraries = IdeaLibrary.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': lib.id,
        'name': lib.name,
        'description': lib.description,
        'total_ideas': lib.total_ideas,
        'total_words': lib.total_words,
        'created_at': lib.created_at.isoformat(),
        'is_default': lib.is_default
    } for lib in libraries]), 200

@bp.route('/libraries', methods=['POST'])
def create_library():
    """Create a new idea library"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    library = IdeaLibrary(
        user_id=user_id,
        name=data.get('name', 'New Library'),
        description=data.get('description', ''),
        is_default=data.get('is_default', False)
    )
    
    db.session.add(library)
    db.session.commit()
    
    return jsonify({'message': 'Library created', 'id': library.id}), 201

@bp.route('/<library_id>', methods=['GET'])
def get_ideas(library_id):
    """Get all ideas in a library"""
    library = IdeaLibrary.query.get(library_id)
    
    if not library:
        return jsonify({'error': 'Library not found'}), 404
    
    # Get root ideas (parent_id is None)
    ideas = Idea.query.filter_by(library_id=library_id, parent_id=None).all()
    
    return jsonify([{
        'id': idea.id,
        'title': idea.title,
        'content': idea.content,
        'status': idea.status,
        'created_at': idea.created_at.isoformat(),
        'word_count': idea.word_count
    } for idea in ideas]), 200

@bp.route('/<library_id>', methods=['POST'])
def create_idea(library_id):
    """Create a new idea"""
    data = request.get_json()
    
    library = IdeaLibrary.query.get(library_id)
    if not library:
        return jsonify({'error': 'Library not found'}), 404
    
    idea = Idea(
        library_id=library_id,
        parent_id=data.get('parent_id'),
        title=data.get('title', 'Untitled'),
        content=data.get('content', '')
    )
    
    # Calculate word count
    if idea.content:
        idea.word_count = len(idea.content.split())
    
    db.session.add(idea)
    db.session.commit()
    
    # Update library statistics
    library.total_ideas += 1
    library.total_words += idea.word_count
    db.session.commit()
    
    return jsonify({'message': 'Idea created', 'id': idea.id}), 201

@bp.route('/<idea_id>', methods=['PUT'])
def update_idea(idea_id):
    """Update an idea"""
    idea = Idea.query.get(idea_id)
    
    if not idea:
        return jsonify({'error': 'Idea not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        idea.title = data['title']
    if 'content' in data:
        old_word_count = idea.word_count
        idea.content = data['content']
        idea.word_count = len(idea.content.split()) if idea.content else 0
        
        # Update library word count
        library = idea.library
        library.total_words = library.total_words - old_word_count + idea.word_count
    if 'status' in data:
        idea.status = data['status']
    if 'ai_thoughts' in data:
        idea.ai_thoughts = data['ai_thoughts']
    
    db.session.commit()
    
    return jsonify({'message': 'Idea updated'}), 200

@bp.route('/<idea_id>', methods=['DELETE'])
def delete_idea(idea_id):
    """Delete an idea"""
    idea = Idea.query.get(idea_id)
    
    if not idea:
        return jsonify({'error': 'Idea not found'}), 404
    
    library = idea.library
    library.total_ideas -= 1
    library.total_words -= idea.word_count
    
    db.session.delete(idea)
    db.session.commit()
    
    return jsonify({'message': 'Idea deleted'}), 200
