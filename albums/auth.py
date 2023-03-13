import jwt

from flask import jsonify, request
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash

from albums import app
from albums.models.users import Users

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split("Bearer ")[1].strip()
        if not token:
            return jsonify('A valid Token is required'), 400
        
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data['id']).first()
            if not current_user: # edge case where User used to exist but was deleted. In this case, we should invalidate the Token
                return jsonify('User not found'), 400
        except jwt.exceptions.InvalidSignatureError:
            return jsonify('Token is invalid'), 400
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify('Token is expired'), 400
 
        return f(*args, **kwargs)
    
    return decorator