import traceback
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError
from werkzeug.exceptions import (
    HTTPException,
    Unauthorized,
    Forbidden,
    BadRequest,
    NotFound,
    MethodNotAllowed,
    Conflict,
)


def register_error_handlers(app, db):

    # --------------------------------------------------------------------------
    # Werkzeug HTTPエラーハンドラ (4xx系クライアントエラー)
    # --------------------------------------------------------------------------
    # これらは `abort(400, "message")` や、Flaskが自動で送出する際に捕捉される。

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        """
        400 Bad Request: リクエストの形式が不正な場合 (例: JSONのパース失敗など)
        """
        app.logger.info(f"BadRequest: {error.description}")
        response = {"error": "Bad Request", "message": error.description}
        return jsonify(response), 400


    @app.errorhandler(Unauthorized)
    def handle_unauthorized(error):
        """
        401 Unauthorized: 認証が必要なリソースに対して、認証情報がないか無効な場合
        """
        app.logger.info(f"Unauthorized: {error.description}")
        # WWW-Authenticateヘッダはエラーオブジェクトから取得できる場合がある
        response = {"error": "Unauthorized", "message": error.description}
        return jsonify(response), 401


    @app.errorhandler(Forbidden)
    def handle_forbidden(error):
        """
        403 Forbidden: 認証はされているが、リソースへのアクセス権限がない場合
        """
        app.logger.warning(f"Forbidden: {error.description}")
        response = {"error": "Forbidden", "message": error.description}
        return jsonify(response), 403


    @app.errorhandler(NotFound)
    def handle_not_found(error):
        """
        404 Not Found: リクエストされたURL/リソースが見つからない場合
        """
        app.logger.info(f"NotFound: {error.description}")
        response = {"error": "Not Found", "message": error.description}
        return jsonify(response), 404


    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
        """
        405 Method Not Allowed: 許可されていないHTTPメソッドでアクセスされた場合
        """
        app.logger.info(f"MethodNotAllowed: {error.description}")
        response = {"error": "Method Not Allowed", "message": error.description}
        return jsonify(response), 405


    @app.errorhandler(Conflict)
    def handle_conflict(error):
        """
        409 Conflict: アプリケーションのビジネスロジックレベルでのリソースの競合
        (例: `raise Conflict("この名前は既に使用されています")`)
        """
        app.logger.info(f"Conflict: {error.description}")
        response = {"error": "Conflict", "message": error.description}
        return jsonify(response), 409


    # --------------------------------------------------------------------------
    # アプリケーション固有のエラーハンドラ
    # --------------------------------------------------------------------------

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """
        422 Unprocessable Entity: Pydanticによるリクエストデータのバリデーション失敗
        """
        app.logger.info(f"Pydantic ValidationError: {error.errors()}")
        response = {"error": "Validation Error", "details": error.errors()}
        return jsonify(response), 422


    # これはSQLAlchemyのデータベースで発生したエラーだが、実はクライアントサイドのエラーと考えることができる。
    # なぜなら、クライアントが送信したデータが、現在のデータベースの状態と矛盾（競合）していることが原因だから。
    # クライアントはリクエスト内容を修正することで、このエラーを解決できる可能性がある。よって、409 Conflictが適切。
    # エラーを分類する際、「どこで発生したか」よりも「何が原因で発生したか」を重視する！！
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        """
        409 Conflict: SQLAlchemyの制約違反 (一意性制約など)
        """
        db.session.rollback()
        app.logger.warning(f"IntegrityError: {error.orig}")
        response = {
            "error": "Conflict",
            "message": "A resource with the same unique data already exists.",
        }
        return jsonify(response), 409


    # --------------------------------------------------------------------------
    # サーバーサイドのエラーハンドラ (5xx系)
    # --------------------------------------------------------------------------

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        """
        500 Internal Server Error: IntegrityError以外のSQLAlchemy関連エラー
        (DB接続エラーなど)
        """
        db.session.rollback()
        app.logger.error(f"SQLAlchemyError: {error}")
        # 本番環境では詳細なエラーメッセージをクライアントに返さない
        response = {
            "error": "Database Error",
            "message": "An unexpected database error occurred.",
        }
        return jsonify(response), 500


    # --------------------------------------------------------------------------
    # フォールバック (最終的なセーフティネット)
    # --------------------------------------------------------------------------

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """
        個別に定義されていない他のWerkzeug HTTPエラーを汎用的に処理する
        """
        app.logger.info(f"HTTPException: {error.code} {error.name}")
        response = {"error": error.name, "message": error.description}
        return jsonify(response), error.code


    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        """
        最終的なフォールバック: これまで捕捉されなかった全ての予期せぬエラーを処理する
        """
        # スタックトレースを含めて詳細なエラーをログに出力する
        tb = traceback.format_exc()
        app.logger.error(f"Unhandled Exception: {error}\n{tb}")

        # 本番環境では、セキュリティのため、クライアントには汎用的なメッセージのみを返す
        # デバッグモードの場合は詳細を返してもよい
        if app.config.get("DEBUG"):
            response = {
                "error": "Internal Server Error",
                "message": str(error),
                "trace": tb.splitlines()
            }
        else:
            response = {
                "error": "Internal Server Error",
                "message": "An unexpected internal error occurred. The administrators have been notified.",
            }
        return jsonify(response), 500