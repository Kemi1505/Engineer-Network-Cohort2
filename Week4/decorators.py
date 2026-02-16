from functools import wraps
from flask import request, jsonify
from auth import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Missing Token'}), 401
        try:
            # Remove 'Bearer ' if present
            token = token.split(' ')[1] if token.startswith('Bearer ') else token
            payload = decode_token(token)
            if not payload:
                return jsonify({'message': 'Invalid or expired token'}), 401
            # Add user info to request
            request.user_id = payload['user_id']
            request.user_role = payload['role']
        except Exception as e:
            return jsonify({'message': 'Invalid Token'}), 401
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'user_role') or request.user_role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated