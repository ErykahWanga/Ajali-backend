# /app/routes/auth_routes.py

from flask import Blueprint, request, jsonify
from ..services import auth_service
from flask_jwt_extended import create_access_token
from ..models import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Missing username, email, or password"}), 400
    
    user = auth_service.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    if not user:
        return jsonify({"msg": "Username or email already exists"}), 409
        
    return jsonify({"msg": "User created successfully", "user": user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400
        
    user = auth_service.authenticate_user(
        username=data['username'],
        password=data['password']
    )
    
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401
    
    # Create a new token with additional claims
    additional_claims = {"is_admin": user.is_admin}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    return jsonify(access_token=access_token)