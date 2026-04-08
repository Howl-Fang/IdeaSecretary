from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Idea, User
import openai

bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@bp.route('/organize', methods=['POST'])
def organize_idea():
    """Use AI to organize and enhance an idea"""
    data = request.get_json()
    user_id = data.get('user_id')
    idea_id = data.get('idea_id')
    content = data.get('content', '')
    
    # Get user's OpenAI API configuration
    user = User.query.get(user_id)
    if not user or not user.openai_api_key:
        return jsonify({'error': 'OpenAI API key not configured'}), 400
    
    # Configure OpenAI client
    api_base = user.openai_api_base or current_app.config['OPENAI_API_BASE']
    openai.api_key = user.openai_api_key
    openai.api_base = api_base
    
    # System prompt for organizing ideas
    system_prompt = """You are an AI assistant specialized in organizing and enhancing ideas.
Your tasks:
1. Analyze the user's input (text, image descriptions, URLs, etc.)
2. Extract key concepts and organize them hierarchically
3. Suggest improvements and related ideas
4. Provide insights and new perspectives

Format your response as JSON with:
- "organized_content": The organized and enhanced content in markdown
- "insights": Key insights and thoughts
- "suggestions": Suggestions for further development
- "related_topics": Related topics that could be explored
"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please organize this idea:\n{content}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        ai_response = response.choices[0].message['content']
        
        # If idea_id provided, update the idea with AI thoughts
        if idea_id:
            idea = Idea.query.get(idea_id)
            if idea:
                idea.ai_thoughts = ai_response
                idea.status = 'organized'
                db.session.commit()
        
        return jsonify({
            'message': 'Idea organized successfully',
            'response': ai_response
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'AI processing failed: {str(e)}'}), 500

@bp.route('/inspire', methods=['POST'])
def get_inspiration():
    """Get AI-generated inspiration based on existing ideas"""
    data = request.get_json()
    library_id = data.get('library_id')
    
    # Get recent ideas from library
    from app.models import IdeaLibrary
    library = IdeaLibrary.query.get(library_id)
    if not library:
        return jsonify({'error': 'Library not found'}), 404
    
    user = User.query.get(library.user_id)
    if not user or not user.openai_api_key:
        return jsonify({'error': 'OpenAI API key not configured'}), 400
    
    # Get recent ideas
    recent_ideas = Idea.query.filter_by(library_id=library_id).order_by(Idea.created_at.desc()).limit(5).all()
    ideas_summary = "\n".join([f"- {idea.title}: {idea.content[:100]}" for idea in recent_ideas])
    
    # Configure OpenAI client
    api_base = user.openai_api_base or current_app.config['OPENAI_API_BASE']
    openai.api_key = user.openai_api_key
    openai.api_base = api_base
    
    system_prompt = """You are a creative AI assistant that generates inspiring ideas and perspectives.
Based on the user's existing ideas, suggest new directions, connections, and inspiration for their knowledge base."""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Based on these ideas:\n{ideas_summary}\n\nGenerate some inspiring suggestions and new perspectives."}
            ],
            temperature=0.9,
            max_tokens=1500
        )
        
        return jsonify({
            'inspiration': response.choices[0].message['content']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Inspiration generation failed: {str(e)}'}), 500

@bp.route('/search', methods=['GET'])
def search_ideas():
    """Search ideas using semantic search"""
    query = request.args.get('q', '')
    library_id = request.args.get('library_id')
    
    if not query or not library_id:
        return jsonify({'error': 'Missing query or library_id'}), 400
    
    # Simple full-text search (can be enhanced with better search algorithms)
    from sqlalchemy import or_
    ideas = Idea.query.filter_by(library_id=library_id).filter(
        or_(
            Idea.title.ilike(f'%{query}%'),
            Idea.content.ilike(f'%{query}%')
        )
    ).all()
    
    return jsonify([{
        'id': idea.id,
        'title': idea.title,
        'content': idea.content[:200],
        'created_at': idea.created_at.isoformat()
    } for idea in ideas]), 200
