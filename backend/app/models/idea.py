from app import db
from datetime import datetime
import uuid

class Idea(db.Model):
    """Idea model - individual idea entry"""
    __tablename__ = 'ideas'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    library_id = db.Column(db.String(36), db.ForeignKey('idea_libraries.id'), nullable=False, index=True)
    
    # Hierarchy
    parent_id = db.Column(db.String(36), db.ForeignKey('ideas.id'), nullable=True, index=True)
    
    # Content
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)  # Markdown format
    ai_thoughts = db.Column(db.Text, nullable=True)  # AI-generated insights
    
    # Status
    status = db.Column(db.String(20), default='draft')  # 'draft', 'organized', 'refined'
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    word_count = db.Column(db.Integer, default=0)
    
    # Relationships
    children = db.relationship('Idea', backref=db.backref('parent', remote_side=[id]), lazy=True, cascade='all, delete-orphan')
    media_relations = db.relationship('MediaResource', backref='idea', lazy=True, secondary='idea_media_association')
    
    def __repr__(self):
        return f'<Idea {self.title}>'
