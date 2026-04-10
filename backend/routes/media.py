from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, MediaIndex, Idea, User
from datetime import datetime
import os
import uuid
import mimetypes

media_bp = Blueprint('media', __name__)

UPLOAD_FOLDER = 'media_storage'
TRASH_FOLDER = 'media_storage/trash'

def ensure_upload_folders():
    """Ensure upload directories exist"""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(TRASH_FOLDER, exist_ok=True)

@media_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_media():
    """Upload media file"""
    user_id = get_jwt_identity()
    ensure_upload_folders()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Generate UUID for filename
    file_uuid = str(uuid.uuid4())
    original_name = file.filename
    
    # Get file extension
    ext = os.path.splitext(original_name)[1]
    filename = f"{file_uuid}{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Save file
    file.save(filepath)
    
    # Get file size
    file_size = os.path.getsize(filepath)
    mime_type = file.content_type or mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
    
    # Create media index entry
    media = MediaIndex(
        user_id=user_id,
        filename=original_name,
        file_path=filepath,
        mime_type=mime_type,
        file_size=file_size
    )
    
    db.session.add(media)
    db.session.commit()
    
    return jsonify({
        'id': media.id,
        'filename': original_name,
        'file_path': media.file_path,
        'mime_type': mime_type,
        'file_size': file_size,
        'created_at': media.created_at.isoformat()
    }), 201

@media_bp.route('/<media_id>', methods=['GET'])
@jwt_required()
def get_media(media_id):
    """Get media file"""
    user_id = get_jwt_identity()
    media = MediaIndex.query.filter_by(id=media_id, user_id=user_id, status='active').first()
    
    if not media:
        return jsonify({'error': 'Media not found'}), 404
    
    if not os.path.exists(media.file_path):
        return jsonify({'error': 'File not found on disk'}), 404
    
    return send_file(media.file_path, mimetype=media.mime_type)

@media_bp.route('/<media_id>', methods=['DELETE'])
@jwt_required()
def delete_media(media_id):
    """Delete media (move to trash)"""
    user_id = get_jwt_identity()
    media = MediaIndex.query.filter_by(id=media_id, user_id=user_id, status='active').first()
    
    if not media:
        return jsonify({'error': 'Media not found'}), 404
    
    ensure_upload_folders()
    
    # Move to trash
    if os.path.exists(media.file_path):
        trash_path = os.path.join(TRASH_FOLDER, f"{media_id}_{os.path.basename(media.file_path)}")
        os.rename(media.file_path, trash_path)
    
    media.status = 'trash'
    media.deleted_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'message': 'Media moved to trash'}), 200

@media_bp.route('/trash', methods=['GET'])
@jwt_required()
def get_trash():
    """Get media in trash"""
    user_id = get_jwt_identity()
    trashed = MediaIndex.query.filter_by(user_id=user_id, status='trash').all()
    
    return jsonify({
        'trash': [{
            'id': m.id,
            'filename': m.filename,
            'deleted_at': m.deleted_at.isoformat()
        } for m in trashed]
    }), 200

@media_bp.route('/trash/cleanup', methods=['POST'])
@jwt_required()
def cleanup_trash():
    """Clean up old trash files"""
    user_id = get_jwt_identity()
    trashed = MediaIndex.query.filter_by(user_id=user_id, status='trash').all()
    
    ensure_upload_folders()
    
    count = 0
    for media in trashed:
        # Delete files older than 30 days (can be configured)
        days_ago = (datetime.utcnow() - media.deleted_at).days
        if days_ago > 30:
            if os.path.exists(media.file_path):
                os.remove(media.file_path)
            db.session.delete(media)
            count += 1
    
    db.session.commit()
    
    return jsonify({'message': f'Cleaned up {count} old files'}), 200

@media_bp.route('/info', methods=['GET'])
@jwt_required()
def get_media_list():
    """Get all user media"""
    user_id = get_jwt_identity()
    media_list = MediaIndex.query.filter_by(user_id=user_id, status='active').all()
    
    return jsonify({
        'media': [{
            'id': m.id,
            'filename': m.filename,
            'mime_type': m.mime_type,
            'file_size': m.file_size,
            'created_at': m.created_at.isoformat()
        } for m in media_list],
        'total_files': len(media_list),
        'total_size': sum(m.file_size for m in media_list)
    }), 200
