from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Idea, SearchIndex, IdeaBase

search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['GET'])
@jwt_required()
def search_ideas():
    """Search ideas by query"""
    user_id = get_jwt_identity()
    query = request.args.get('q', '').strip()
    base_id = request.args.get('base_id')
    limit = request.args.get('limit', 20, type=int)
    
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    # Search in search index
    search_query = SearchIndex.query.join(Idea).join(IdeaBase).filter(
        IdeaBase.user_id == user_id,
        SearchIndex.search_text.ilike(f'%{query}%')
    )
    
    if base_id:
        search_query = search_query.filter(Idea.idea_base_id == base_id)
    
    results = search_query.limit(limit).all()
    
    return jsonify({
        'results': [{
            'idea_id': r.idea_id,
            'idea': {
                'title': r.idea.title,
                'content': r.idea.content[:200],  # Preview
                'created_at': r.idea.created_at.isoformat()
            }
        } for r in results],
        'count': len(results)
    }), 200
