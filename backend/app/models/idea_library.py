from app import db
from datetime import datetime
import uuid

class IdeaLibrary(db.Model):
    """Idea Library model - collection of ideas"""
    __tablename__ = 'idea_libraries'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Statistics
    total_ideas = db.Column(db.Integer, default=0)
    total_words = db.Column(db.Integer, default=0)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Configuration
    is_default = db.Column(db.Boolean, default=False)
    
    # Relationships
    ideas = db.relationship('Idea', backref='library', lazy=True, cascade='all, delete-orphan')
    media_resources = db.relationship('MediaResource', backref='library', lazy=True, cascade='all, delete-orphan')
    index_records = db.relationship('IndexRecord', backref='library', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<IdeaLibrary {self.name}>'
