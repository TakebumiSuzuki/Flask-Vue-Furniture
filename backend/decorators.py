from functools import wraps
from flask import request, current_app
from werkzeug.exceptions import BadRequest, Forbidden
from flask_jwt_extended import current_user, jwt_required


def json_required(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        # request.get_json(silent=True) はJSONのパースに失敗した場合、例外を発生させずにNoneを返す。
        data = request.get_json(silent=True)

        # dataがNoneの場合（JSONがない、または形式が不正）、エラーを返す
        if data is None:
            current_app.logger.info('Request body must be valid JSON.')
            raise BadRequest('Request body must be valid JSON.')

        kwargs['payload'] = data

        return func(*args, **kwargs)

    return decorated_function


def admin_required(fn):

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            raise Forbidden("Admin role is needed for this endpoint.")
        return fn(*args, **kwargs)

    return wrapper