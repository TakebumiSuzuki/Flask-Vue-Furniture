from flask import Blueprint, request, jsonify, url_for
from backend.schemas.user import CreateUser, PublicUser
from backend.models.user import User
from backend.extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/users')


@auth_bp.post('')
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must contain JSON data.'}), 400
    data = CreateUser.model_validate(data).model_dump()
    user = User(**data)
    user.set_password_hash(user.password)
    db.session.add(user)
    db.session.commit()
    output = PublicUser.model_validate(user).model_dump()

    return jsonify({
        'message':'Successfully new user created!',
        'user': output
    }), 201, {'Location': url_for('auth.get_user', usr_id=output['id'], _external=True)}