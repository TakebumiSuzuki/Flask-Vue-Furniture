from flask import Blueprint, jsonify, url_for, request
from werkzeug.exceptions import NotFound
from sqlalchemy import select, desc, asc, or_
from backend.extensions import db
from backend.models.furniture import Furniture
from backend.schemas.furniture import PublicFurniture
import time


furnitures_bp = Blueprint('furnitures', __name__, url_prefix='/api/v1/furnitures')

@furnitures_bp.get('')
def get_furnitures():
    time.sleep(0.5)

    query = request.args.get('q')
    sort = request.args.get('sort')
    order = request.args.get('order')
    try:
        page = int(request.args.get('page', 1)) # デフォルトを1として整数に変換
        if page < 1: page = 1
    except (ValueError, TypeError):
        page = 1 # 整数に変換できない場合は1ページ目にする

    PER_PAGE = 2

    stmt = select(Furniture)
    column = None

    if sort and order:
        sort_map = {
            'price': Furniture.price,
            'created': Furniture.created_at,
            'updated': Furniture.updated_at
        }
        column = sort_map.get(sort)

    if column:
        if order.lower() in ['desc']:
            stmt = stmt.order_by(desc(column))
        else:
            stmt = stmt.order_by(asc(column))
    else:
        stmt = stmt.order_by(desc(Furniture.updated_at))

    if query:
        stmt = stmt.where(or_(
            Furniture.name.ilike(f'%{query}%'),
            Furniture.description.ilike(f'%{query}%'),
            Furniture.color.ilike(f'{query}%')
        ))

    try:
        pagination = db.paginate(stmt, page=page, per_page=PER_PAGE, error_out=True)
    except:
        # ページ番号が範囲外の場合（例：総ページ数を超えた場合）に404エラーを返す
        return jsonify({'message': 'Page not found', 'error_code':'PAGE_NOT_FOUND'}), 404

    furnitures = pagination.items

    print(furnitures)
    output = [PublicFurniture.model_validate(furniture).model_dump() for furniture in furnitures]

    return jsonify({
        'furnitures': output,
        'total_items': pagination.total,
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200


@furnitures_bp.get('/<int:id>')
def get_furniture(id):
    time.sleep(0.5)

    # DB接続エラーなどの場合には、sal_alchemyの例外が排出される。
    # IDに対応するレコードが見つからなかった場合にはNoneが返される
    furniture = db.session.get(Furniture, id)
    if furniture is None:
        # Flaskに組み込まれた404エラーを発生させるのが最も一般的でクリーンな方法です
        raise NotFound(f'Furniture with id {id} not found.')
    output = PublicFurniture.model_validate(furniture).model_dump()

    return jsonify(output), 200



