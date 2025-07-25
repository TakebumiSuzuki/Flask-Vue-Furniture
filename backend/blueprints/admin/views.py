from flask import Blueprint, jsonify
from sqlalchemy import select

from backend.models.user import User
from backend.schemas.user import ReadUser
from backend.extensions import db
from backend.decorators import admin_required
from werkzeug.exceptions import NotFound

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.get('/users')
@admin_required
def get_userlist():
    stmt = select(User).order_by(User.last_login_at.desc())
    users = db.session.execute(stmt).scalars().all()
    output = [ ReadUser.model_validate(user).model_dump() for user in users]

    return jsonify({'users': output}), 200


@admin_bp.patch('/users/<string:user_id>/change-role')
@admin_required
def change_role(user_id):
    user = db.session.get(User, user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    # クライアント側ではUIだけ変えておく。ページリロードはしなくて良いと考えられる
    # APIリクエストが失敗した際には、UIを操作前の状態に戻す（例: 削除しようとした行を再表示する、変更した役割の表示を元に戻す）エラーハンドリング処理をクライアント側で必ず実装する必要があります。
    return jsonify({}), 200


@admin_bp.delete('/users/<string:user_id>/delete-user')
@admin_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        raise NotFound('User with the specified ID was not found.')
    db.session.delete(user)
    db.session.commit()
    # クライアント側ではUIだけ変えておく。ページリロードはしなくて良いと考えられる
    return jsonify({}), 204