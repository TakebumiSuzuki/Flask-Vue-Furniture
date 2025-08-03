from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required, unset_jwt_cookies

from werkzeug.exceptions import Unauthorized, Conflict

from backend.decorators import json_required
from backend.models.user import User
from backend.extensions import db
from backend.schemas.user import PublicUser, ChangeUsernameUser, ChangePasswordUser

import time

# ここでしている'/account'はあくまでデフォルトで、app.register_blueprint(account_bp, url_prefix='/api/v1/account')
# により、完全に上書きされる。結合はされない。よってこの場合、'/account'は意味をなさない
account_bp = Blueprint('account', __name__, url_prefix='/account')

# current_userについて:もしユーザーが見つからなければ、Flask-JWT-Extendedが自動的に
# 401 Unauthorized エラーを返してくれるため、関数本体に処理が到達した時点では
# current_user には必ずユーザーオブジェクトが格納されている、と考えて問題ありません。

@account_bp.get('')
@jwt_required()
def get_user():
    time.sleep(1)

    output = PublicUser.model_validate(current_user).model_dump()
    return jsonify({'user': output}), 200


@account_bp.delete('')
@jwt_required()
def delete_user():
    time.sleep(1)

    # Blocklistにrefresh_tokenを登録する必要はない。つまりそもそもrefresh_tokenをいじる必要はない。
    # なぜなら User Lookup loaderによって、Userを見つけられずにエラーになりそこで弾かれるので。

    db.session.delete(current_user)
    db.session.commit()

    response = jsonify({'message': 'Account deleted successfully.'})
    unset_jwt_cookies(response)
    # クライアント側でアクセストークンを消去するのを忘れずに！
    return response, 200


@account_bp.patch('/update-username')
@jwt_required()
@json_required
def username_change(payload):
    time.sleep(1)

    dto = ChangeUsernameUser.model_validate(payload)

    if User.get_user_by_username(payload['username']):
        raise Conflict('This username already exists.')

    current_user.username = dto.username
    db.session.commit()
    return jsonify({}), 200


@account_bp.patch('/update-password')
@jwt_required()
@json_required
def password_update(payload):
    time.sleep(1)

    dto = ChangePasswordUser.model_validate(payload)

    if not current_user.check_password_match(dto.old_password):
        raise Unauthorized('Old password is not correct.')

    current_user.set_password_hash(dto.new_password)
    current_user.update_token_valid_after()

    db.session.commit()

    response = jsonify({})
    unset_jwt_cookies(response)

    # クライアント側でアクセストークンを消去するのを忘れずに！
    return response, 200
