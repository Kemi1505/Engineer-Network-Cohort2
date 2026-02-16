# Authentication functions
import jwt
import os
from datetime import datetime, timedelta, timezone

ACCESS_SECRET = os.getenv('JWT_ACCESS_SECRET')
REFRESH_SECRET = os.getenv('JWT_REFRESH_SECRET')
ACCESS_EXPIRY = int(os.getenv('JWT_ACCESS_EXPIRY_MINUTES', 15))
REFRESH_EXPIRY = int(os.getenv('JWT_REFRESH_EXPIRY_DAYS', 7))

def create_access_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRY),
        'type': 'access'
    }
    return jwt.encode(payload, ACCESS_SECRET, algorithm='HS256')

def create_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=REFRESH_EXPIRY),
        'type': 'refresh'
    }
    return jwt.encode(payload, REFRESH_SECRET, algorithm='HS256')

def decode_token(token, is_refresh=False):
    secret = REFRESH_SECRET if is_refresh else ACCESS_SECRET
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Expired token
    except jwt.InvalidTokenError:
        return None  # Invalid token