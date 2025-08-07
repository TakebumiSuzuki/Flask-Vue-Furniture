from uuid import UUID
from flask import Blueprint, jsonify, url_for, current_app
from werkzeug.exceptions import Unauthorized, Conflict, BadRequest
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, set_refresh_cookies, unset_refresh_cookies, get_jwt_identity, get_jwt
from backend.decorators import json_required
from backend.extensions import db
from backend.models.user import User
from backend.schemas.user import CreateUser, PublicUser
from backend.models.blocked_token import BlockedToken
import time

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.post('/registration')
@json_required
def create_user(payload):
    time.sleep(0.5)

    dto = CreateUser.model_validate(payload).model_dump()
    user = User(**dto)
    existing_user = User.get_user_by_username(user.username)
    existing_email = User.get_user_by_email(user.email)
    if existing_user:
        raise Conflict('This username is already taken.')
    if existing_email:
        raise Conflict('This email already exists.')
    user.set_password_hash(user.password)
    # user.is_admin = True #アドミン設定　
    db.session.add(user)
    db.session.commit()
    output = PublicUser.model_validate(user).model_dump()

    return jsonify({ 'user': output }), 201, {'Location': url_for('account.get_user', _external=True)}


@auth_bp.post('/login')
@json_required
def login(payload):
    time.sleep(0.5)

    if 'email' not in payload or 'password' not in payload:
        raise BadRequest('Email and password are required')
    user = User.get_user_by_email(payload['email'])
    if user and user.check_password_match(payload['password']):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        user.update_last_login_at()
        db.session.commit()
        output = PublicUser.model_validate(user).model_dump()

        response_body = jsonify({
            'user': output,
            'access_token': access_token,
        })
        set_refresh_cookies(response_body, refresh_token)
        return response_body, 200

    else:
        raise Unauthorized('Enter the correct email and password.')


@auth_bp.post('/logout')
@jwt_required(refresh=True, locations=["cookies"])
def logout():
    time.sleep(0.5)

    refresh_jti = get_jwt()['jti']
    blocked_token = BlockedToken(jti=refresh_jti)
    db.session.add(blocked_token)
    db.session.commit()
    response_body = jsonify({})
    unset_refresh_cookies(response_body)
    # クライアントサイドでアクセストークンの消去も忘れずに
    return response_body, 200


@auth_bp.post('/refresh-tokens')
# このlocations=["cookies"]のおかげでJWT_TOKEN_LOCATION = ['headers', 'cookies']が上書きされ、
# これにより、クライアントサイドのaxiosのインターセプターが簡潔に書けるようになる。
# ちなみに、@jwt_required() (または jwt_required(refresh=False) と同等) は、アクセストークンのみを有効とみなす。
@jwt_required(refresh=True, locations=["cookies"])
def refresh_tokens():
    time.sleep(0.5)

    refresh_jti = get_jwt()['jti']
    blocked_token = BlockedToken(jti=refresh_jti)
    db.session.add(blocked_token)
    db.session.commit()

    identity = get_jwt_identity()
    access_token = create_access_token(identity)
    refresh_token = create_refresh_token(identity)

    user = db.session.get(User, UUID(identity))
    user.update_last_login_at()
    db.session.commit()
    output = PublicUser.model_validate(user).model_dump()
    print(f'ユーザー情報 {output}')
    response_body = jsonify({ 'access_token': access_token, 'user': output })
    set_refresh_cookies(response_body, refresh_token)
    return response_body, 200

