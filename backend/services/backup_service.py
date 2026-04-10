import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from models import db, User, Backup

BACKUP_FOLDER = 'backups'

class BackupService:
    """Service for managing user backups"""
    
    @staticmethod
    def ensure_backup_folder():
        """Ensure backup directory exists"""
        os.makedirs(BACKUP_FOLDER, exist_ok=True)
    
    @staticmethod
    def should_backup(user: User) -> bool:
        """Check if user has reached backup threshold (10 operations)"""
        return user.operation_count % 10 == 0 and user.operation_count > 0
    
    @staticmethod
    def create_backup(user: User) -> bool:
        """Create backup for user database"""
        try:
            BackupService.ensure_backup_folder()
            
            # Create user backup folder
            user_backup_dir = os.path.join(BACKUP_FOLDER, user.id)
            os.makedirs(user_backup_dir, exist_ok=True)
            
            # Create timestamped backup file
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"backup_{timestamp}.zip"
            backup_path = os.path.join(user_backup_dir, backup_filename)
            
            # Export user data as ZIP
            from io import BytesIO
            import zipfile
            import json
            
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Export all user ideas
                ideas_data = []
                from models import IdeaBase, Idea
                
                for base in user.idea_bases:
                    base_data = {
                        'id': base.id,
                        'name': base.name,
                        'description': base.description,
                        'ideas': BackupService._export_ideas(base.ideas)
                    }
                    ideas_data.append(base_data)
                
                # Add JSON file to zip
                zf.writestr('ideas.json', json.dumps(ideas_data, indent=2, default=str))
                
                # Add user metadata
                metadata = {
                    'user_id': user.id,
                    'username': user.username,
                    'backup_date': datetime.utcnow().isoformat(),
                    'operation_count': user.operation_count
                }
                zf.writestr('metadata.json', json.dumps(metadata, indent=2))
            
            # Write ZIP to disk
            with open(backup_path, 'wb') as f:
                f.write(zip_buffer.getvalue())
            
            # Get file size
            backup_size = os.path.getsize(backup_path)
            
            # Record backup in database
            backup_record = Backup(
                user_id=user.id,
                backup_path=backup_path,
                backup_size=backup_size,
                operation_count=user.operation_count
            )
            db.session.add(backup_record)
            
            # Clean up old backups (keep only last 5)
            BackupService.cleanup_old_backups(user)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Backup error: {str(e)}")
            return False
    
    @staticmethod
    def _export_ideas(ideas, parent_data=None):
        """Recursively export ideas tree"""
        if parent_data is None:
            parent_data = []
        
        for idea in ideas:
            idea_data = {
                'id': idea.id,
                'title': idea.title,
                'content': idea.content,
                'ai_thought': idea.ai_thought,
                'tags': idea.tags,
                'content_type': idea.content_type,
                'created_at': idea.created_at.isoformat(),
                'updated_at': idea.updated_at.isoformat(),
                'children': []
            }
            
            if idea.children:
                BackupService._export_ideas(idea.children, idea_data['children'])
            
            parent_data.append(idea_data)
        
        return parent_data
    
    @staticmethod
    def cleanup_old_backups(user: User, keep_count: int = 5):
        """Keep only recent backups"""
        backups = Backup.query.filter_by(user_id=user.id).order_by(Backup.created_at.desc()).all()
        
        for backup in backups[keep_count:]:
            try:
                if os.path.exists(backup.backup_path):
                    os.remove(backup.backup_path)
                db.session.delete(backup)
            except Exception as e:
                print(f"Cleanup error: {str(e)}")
        
        db.session.commit()
    
    @staticmethod
    def increment_operation_count(user: User):
        """Increment operation count and trigger backup if needed"""
        user.operation_count += 1
        db.session.commit()
        
        if BackupService.should_backup(user):
            BackupService.create_backup(user)
    
    @staticmethod
    def get_user_backups(user: User):
        """Get all backups for user"""
        return Backup.query.filter_by(user_id=user.id).order_by(Backup.created_at.desc()).all()
