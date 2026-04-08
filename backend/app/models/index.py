from app import db
from datetime import datetime

class IndexRecord(db.Model):
    """Index Record model - for fast searching"""
    __tablename__ = 'index_records'
    
    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.String(36), db.ForeignKey('idea_libraries.id'), nullable=False, index=True)
    
    # Indexed content
    idea_id = db.Column(db.String(36), db.ForeignKey('ideas.id'), nullable=True, index=True)
    
    # Full-text search index
    search_text = db.Column(db.Text, nullable=False)
    
    # Metadata
    indexed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # For rebalancing
    is_stale = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<IndexRecord for idea {self.idea_id}>'
