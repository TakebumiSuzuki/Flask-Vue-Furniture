from flask import Blueprint, jsonify, url_for
from werkzeug.exceptions import NotFound
from sqlalchemy import select, desc
from backend.extensions import db
from backend.models.furniture import Furniture
from backend.schemas.furniture import PublicFurniture


furnitures_bp = Blueprint('furnitures', __name__, url_prefix='/api/v1/furnitures')

@furnitures_bp.get('')
def get_furnitures():
    stmt = select(Furniture).order_by(desc(Furniture.updated_at))
    furnitures = db.session.execute(stmt).scalars().all()
    output = [PublicFurniture.model_validate(furniture).model_dump() for furniture in furnitures]
    return jsonify(output), 200


@furnitures_bp.get('/<int:id>')
def get_furniture(id):
    # DB接続エラーなどの場合には、sal_alchemyの例外が排出される。
    # IDに対応するレコードが見つからなかった場合にはNoneが返される
    furniture = db.session.get(Furniture, id)
    if furniture is None:
        # Flaskに組み込まれた404エラーを発生させるのが最も一般的でクリーンな方法です
        raise NotFound(f'Furniture with id {id} not found.')
    output = PublicFurniture.model_validate(furniture).model_dump()

    return jsonify(output), 200



