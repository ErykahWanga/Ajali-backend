# /app/services/auth_service.py

from ..models import User
from ..utils.database import db

def create_user(username, email, password):
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return None  # User already exists
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return new_user

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None