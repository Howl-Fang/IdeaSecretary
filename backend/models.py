from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # OpenAI Configuration
    openai_api_key = db.Column(db.String(255), nullable=True)
    openai_api_url = db.Column(db.String(255), nullable=True, default='https://api.openai.com/v1')
    openai_model = db.Column(db.String(100), nullable=True, default='gpt-3.5-turbo')
    
    # Settings
    language = db.Column(db.String(10), default='en')  # 'en' or 'zh'
    dark_mode = db.Column(db.Boolean, default=False)
    operation_count = db.Column(db.Integer, default=0)  # For backup tracking
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    idea_bases = db.relationship('IdeaBase', backref='user', lazy=True, cascade='all, delete-orphan')
    media_indices = db.relationship('MediaIndex', backref='user', lazy=True, cascade='all, delete-orphan')
    backups = db.relationship('Backup', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class IdeaBase(db.Model):
    """Knowledge Base model - default one per user, but can have multiple"""
    __tablename__ = 'idea_bases'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_default = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Statistics
    idea_count = db.Column(db.Integer, default=0)
    total_word_count = db.Column(db.Integer, default=0)
    
    # Relationships
    ideas = db.relationship('Idea', backref='idea_base', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<IdeaBase {self.name}>'

class Idea(db.Model):
    """Idea/Node model - tree structure"""
    __tablename__ = 'ideas'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    idea_base_id = db.Column(db.String(36), db.ForeignKey('idea_bases.id'), nullable=False, index=True)
    parent_id = db.Column(db.String(36), db.ForeignKey('ideas.id'), nullable=True, index=True)
    
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)  # Markdown format
    ai_thought = db.Column(db.Text, nullable=True)  # AI suggestions/analysis
    
    # Tags for organization
    tags = db.Column(db.Text, nullable=True)  # JSON array as string
    
    # Type: 'text', 'image', 'link', 'voice'
    content_type = db.Column(db.String(50), default='text')
    
    # Media references
    media_ids = db.Column(db.Text, nullable=True)  # JSON array of media IDs
    
    # Tree structure
    order = db.Column(db.Integer, default=0)  # For ordering children
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    
    # Relationships
    children = db.relationship('Idea', backref=db.backref('parent', remote_side=[id]), cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Idea {self.title}>'

class MediaIndex(db.Model):
    """Media resource index - uuid named files"""
    __tablename__ = 'media_indices'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # File info
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)  # relative path with UUID
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    
    # Status: 'active', 'trash'
    status = db.Column(db.String(20), default='active')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)  # When moved to trash
    
    def __repr__(self):
        return f'<MediaIndex {self.filename}>'

class Backup(db.Model):
    """Backup records for each user"""
    __tablename__ = 'backups'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    backup_path = db.Column(db.String(500), nullable=False)
    backup_size = db.Column(db.Integer, nullable=False)  # in bytes
    operation_count = db.Column(db.Integer, nullable=False)  # operations count at backup time
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Backup {self.id}>'

class SearchIndex(db.Model):
    """Full-text search index for fast queries"""
    __tablename__ = 'search_index'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    idea_id = db.Column(db.String(36), db.ForeignKey('ideas.id'), nullable=False, index=True)
    
    search_text = db.Column(db.Text, nullable=False)  # Indexed text
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SearchIndex {self.idea_id}>'
