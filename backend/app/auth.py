from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from .extensions import db
from .models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.post('/login')
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get('email', '').lower()).first()
    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'message': 'Credenciales incorrectas'}), 401
    token = create_access_token(identity=str(user.id), additional_claims={'role': user.role, 'name': user.name})
    return jsonify({'accessToken': token, 'user': {'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role}})

@auth_bp.get('/me')
@jwt_required()
def me():
    user = db.session.get(User, int(get_jwt_identity()))
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role})
