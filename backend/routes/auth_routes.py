# /backend/routes/auth_routes.py
from flask import request, jsonify, Blueprint
from models import db, User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Missing username, email, or password"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 409

    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        # Add 'is_admin' claim to the token
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(
            identity=user.id, additional_claims=additional_claims
        )
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad email or password"}), 401