import bcrypt
from models import db, User

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, password_hash):
    """Verify password"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_user(username, email, password):
    """Create new user"""
    if User.query.filter_by(username=username).first():
        return None, 'Username already exists'
    
    if User.query.filter_by(email=email).first():
        return None, 'Email already exists'
    
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)
    )
    
    db.session.add(user)
    db.session.commit()
    
    return user, None

def authenticate_user(username, password):
    """Authenticate user by username and password"""
    user = User.query.filter_by(username=username).first()
    
    if user and verify_password(password, user.password_hash):
        return user
    
    return None
