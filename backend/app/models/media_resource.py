from app import db
from datetime import datetime
import uuid

class MediaResource(db.Model):
    """Media Resource model - images, files, etc."""
    __tablename__ = 'media_resources'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    library_id = db.Column(db.String(36), db.ForeignKey('idea_libraries.id'), nullable=False, index=True)
    
    # File information
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)  # UUID-based path
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    
    # Status
    status = db.Column(db.String(20), default='active')  # 'active' or 'trash'
    
    # Metadata
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # URL if from external source
    url = db.Column(db.String(500), nullable=True)
    
    def __repr__(self):
        return f'<MediaResource {self.filename}>'
