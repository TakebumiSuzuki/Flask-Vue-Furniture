from flask import Blueprint, jsonify, url_for
from sqlalchemy import select, desc
from uuid import UUID

from backend.models.user import User
from backend.schemas.user import ReadUser
from backend.extensions import db
from backend.decorators import admin_required
from werkzeug.exceptions import NotFound

from backend.schemas.furniture import CreateFurniture, ReadFurniture, UpdateFurniture
from backend.decorators import json_required
from backend.models.furniture import Furniture

import time

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


@admin_bp.get('/users')
@admin_required
def get_userlist():
    time.sleep(0.5)

    stmt = select(User).order_by(User.last_login_at.desc())
    users = db.session.execute(stmt).scalars().all()
    output = [ ReadUser.model_validate(user).model_dump() for user in users]

    return jsonify({'users': output}), 200


@admin_bp.get('/users/<string:user_id>')
@admin_required
def get_user(user_id):
    time.sleep(0.5)

    user_id_uuid = UUID(user_id)
    user = db.session.get(User, user_id_uuid)
    output = ReadUser.model_validate(user).model_dump()
    return jsonify({'user': output}), 200


@admin_bp.patch('/users/<string:user_id>/change-role')
@admin_required
def change_role(user_id):
    time.sleep(0.5)

    try:
        user_id_uuid = UUID(user_id)
    except ValueError:
        # そもそもUUIDとして不正な形式の文字列が来た場合
        raise NotFound('Invalid user ID format.')
    user = db.session.get(User, user_id_uuid)
    if not user:
        raise NotFound('User with the specified ID was not found.')

    user.is_admin = not user.is_admin
    db.session.commit()
    # クライアント側ではUIだけ変えておく。ページリロードはしなくて良いと考えられる
    # APIリクエストが失敗した際には、UIを操作前の状態に戻す（例: 削除しようとした行を再表示する、変更した役割の表示を元に戻す）エラーハンドリング処理をクライアント側で必ず実装する必要があります。
    return jsonify({}), 200


@admin_bp.delete('/users/<string:user_id>/delete-user')
@admin_required
def delete_user(user_id):
    time.sleep(0.5)

    try:
        user_id_uuid = UUID(user_id)
    except ValueError:
        # そもそもUUIDとして不正な形式の文字列が来た場合
        raise NotFound('Invalid user ID format.')
    user = db.session.get(User, user_id_uuid)
    if not user:
        raise NotFound('User with the specified ID was not found.')

    if not user:
        raise NotFound('User with the specified ID was not found.')
    db.session.delete(user)
    db.session.commit()
    # クライアント側ではUIだけ変えておく。ページリロードはしなくて良いと考えられる
    return jsonify({}), 204




### furnitures
@admin_bp.post('/furnitures')
@admin_required
@json_required
def create_furniture(payload):
    time.sleep(0.5)

    dto = CreateFurniture.model_validate(payload)

    # Pydanticモデルを一度、辞書に変換する
    # ここで問題！dto.model_dump() が HttpUrl オブジェクトをそのまま返してしまいエラーになる。これは仕様。
    furniture_data = dto.model_dump()

    # 【ここが重要】HttpUrlオブジェクトを明示的に文字列に変換する
    if furniture_data.get('image_url') is not None:
        furniture_data['image_url'] = str(furniture_data['image_url'])
    # アスタリスクの部分はアンパックと呼ばれ、辞書の前に ** をつけると、この辞書を展開し、キーを引数名、値をその引数の値として渡す。
    # アスタリスクが一つの場合には、リストやタプルを展開して、位置引数として順番に渡す。
    furniture = Furniture(**furniture_data)
    db.session.add(furniture)
    db.session.commit()
    # `model_dump(mode='json')` を使うと、Pydanticは「これからこのデータをJSONにするんだな」と理解し、以下のような特殊な型を自動的にJSONが扱える形式に変換してくれます。`HttpUrl` → `str``EmailStr` → `str``datetime` → `str` (ISO 8601形式の文字列)`Decimal` → `float` または `str` (設定による)`UUID` → `str`
    output = ReadFurniture.model_validate(furniture).model_dump(mode='json')
    location = url_for('admin.get_furniture', id=output['id'], _external=True)

    return jsonify(output), 201, {'Location': location }


@admin_bp.patch('/furnitures/<int:id>')
@admin_required
@json_required
def update_furniture(payload, id):
    time.sleep(0.5)

    # payload と id は、どちらもキーワード引数（kwargs）として渡されるため、引数の順番は問われません。(Furniture, id)でもok.
    furniture = db.session.get(Furniture, id)
    if furniture is None:
        raise NotFound(f'Furniture with id {id} not found.')

    updateData = UpdateFurniture.model_validate(payload).model_dump(exclude_unset=True)
    for key, value in updateData.items():
        setattr(furniture, key, value)
    db.session.commit()
    output = ReadFurniture.model_validate(furniture).model_dump()
    return jsonify(output), 200


@admin_bp.get('/furnitures')
@admin_required
def get_furnitures():
    time.sleep(0.5)

    # もし、order_by を省略すると、データベースが、最も効率的だと判断した順序でデータを返します。
    # データが物理的にディスクに保存されている順序かもしれませんし、何らかのインデックスを利用した結果かもしれません
    stmt = select(Furniture).order_by(desc(Furniture.updated_at))
    # テーブルの結合をした場合や、カラムを複数指定してそれだけを取り出したい場合には、タプルとして表現されたrowオブジェクト
    # のリストが返ってくる。で、ここでは行あたり単一オブジェクトのリストであり、タプルで帰ってきて欲しくないので、scalars()をつける。
    # all()をつけるとリストとして全部が返ってくる。つけないとイテレーターが返ってくる。
    furnitures = db.session.execute(stmt).scalars().all()
    output = [ReadFurniture.model_validate(furniture).model_dump() for furniture in furnitures]

    return jsonify(output), 200


@admin_bp.get('/furnitures/<int:id>')
@admin_required
def get_furniture(id):
    time.sleep(0.5)

    # DB接続エラーなどの場合には、SQLAlchemyの例外が発生される。
    # IDに対応するレコードが見つからなかった場合にはNoneが返される
    furniture = db.session.get(Furniture, id)
    if furniture is None:
        # Flaskに組み込まれた404エラーを発生させるのが最も一般的でクリーンな方法です
        raise NotFound(f'Furniture with id {id} not found.')
    output = ReadFurniture.model_validate(furniture).model_dump()

    return jsonify(output), 200


@admin_bp.delete('/furnitures/<int:id>')
@admin_required
def delete_furniture(id):
    time.sleep(0.5)

    furniture = db.session.get(Furniture, id)
    if furniture is None:
        # Flaskに組み込まれた404エラーを発生させるのが最も一般的でクリーンな方法です
        raise NotFound(f'Furniture with id {id} not found.')

    db.session.delete(furniture)
    db.session.commit()
    # jsonify({}) は空のJSONオブジェクト ({}) のボディと Content-Type: application/json ヘッダーを生成してしまう。
    # 204では、Flaskでボディを含まないレスポンスを返さないといけないので、以下のように '' とするのが一般的。
    return '', 204


