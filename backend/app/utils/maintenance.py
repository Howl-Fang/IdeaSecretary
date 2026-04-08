"""Backup and maintenance utilities"""
import os
import shutil
import json
from datetime import datetime
import zipfile
from pathlib import Path

def backup_database(db_path, backup_folder):
    """Backup the SQLite database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"idea_secretary_backup_{timestamp}.db"
    backup_path = os.path.join(backup_folder, backup_filename)
    
    # Create backup folder if it doesn't exist
    os.makedirs(backup_folder, exist_ok=True)
    
    # Copy database file
    if os.path.exists(db_path):
        shutil.copy2(db_path, backup_path)
        return backup_path
    
    return None

def cleanup_old_backups(backup_folder, keep_count=10):
    """Delete old backup files, keeping only the most recent ones"""
    if not os.path.exists(backup_folder):
        return
    
    backup_files = sorted(
        [f for f in os.listdir(backup_folder) if f.startswith('idea_secretary_backup_') and f.endswith('.db')],
        reverse=True
    )
    
    # Remove old backups
    for old_backup in backup_files[keep_count:]:
        os.remove(os.path.join(backup_folder, old_backup))

def cleanup_trash(trash_folder, days_before_delete=30):
    """Clean up files in trash older than specified days"""
    from datetime import timedelta
    
    if not os.path.exists(trash_folder):
        return
    
    cutoff_date = datetime.now() - timedelta(days=days_before_delete)
    
    for filename in os.listdir(trash_folder):
        filepath = os.path.join(trash_folder, filename)
        if os.path.isfile(filepath):
            file_modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_modified_time < cutoff_date:
                os.remove(filepath)

def export_library_as_zip(library_id, library_obj, media_folder, output_path):
    """Export a knowledge library as a ZIP file with all media"""
    with zipfile.ZipFile(output_path, 'w') as zipf:
        # Export library metadata
        metadata = {
            'id': library_id,
            'name': library_obj.name,
            'description': library_obj.description,
            'created_at': library_obj.created_at.isoformat(),
            'total_ideas': library_obj.total_ideas,
            'total_words': library_obj.total_words
        }
        zipf.writestr('metadata.json', json.dumps(metadata, indent=2))
        
        # Export all ideas
        ideas_data = []
        for idea in library_obj.ideas:
            ideas_data.append({
                'id': idea.id,
                'title': idea.title,
                'content': idea.content,
                'ai_thoughts': idea.ai_thoughts,
                'status': idea.status,
                'created_at': idea.created_at.isoformat(),
                'updated_at': idea.updated_at.isoformat()
            })
        zipf.writestr('ideas.json', json.dumps(ideas_data, indent=2))
        
        # Export media files
        for media in library_obj.media_resources:
            if media.file_path and os.path.exists(media.file_path):
                arcname = f"media/{os.path.basename(media.file_path)}"
                zipf.write(media.file_path, arcname)

def rebalance_index(library_obj):
    """Reorganize and optimize the search index"""
    from app.models import IndexRecord
    from app import db
    
    # Mark all existing index records as stale
    IndexRecord.query.filter_by(library_id=library_obj.id).update({'is_stale': True})
    
    # Regenerate index records for all ideas
    for idea in library_obj.ideas:
        search_text = f"{idea.title} {idea.content or ''}"
        
        # Remove old record if exists
        IndexRecord.query.filter_by(idea_id=idea.id).delete()
        
        # Create new record
        index_record = IndexRecord(
            library_id=library_obj.id,
            idea_id=idea.id,
            search_text=search_text,
            is_stale=False
        )
        db.session.add(index_record)
    
    db.session.commit()
