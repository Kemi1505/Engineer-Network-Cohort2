# all user related routes
import os
from extensions import db, bcrypt, limiter
from flask import request, jsonify, Blueprint
from validation import UserRegisterSchema, UserLoginSchema, ValidationError
from models import User
from auth import create_access_token, create_refresh_token, decode_token
from decorators import token_required

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")

def register():
    schema = UserRegisterSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 409
    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed,
        role='user'  # default role
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@user_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    schema = UserLoginSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

@user_bp.route('/refresh', methods=['POST'])
def refresh():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing Token'}), 401
    token = token.split(' ')[1] if token.startswith('Bearer ') else token

    payload = decode_token(token, is_refresh=True)
    if not payload:
        return jsonify({'message': 'Invalid or expired refresh token'}), 401

    user = User.query.get(payload['user_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    new_access = create_access_token(user.id, user.role)
    return jsonify({'access_token': new_access}), 200

@user_bp.route('/profile', methods=['GET'])
@token_required
def profile():
    user = User.query.get(request.user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at
    }), 200

