from werkzeug.exceptions import Unauthorized
from sqlalchemy import select
from backend.models.user import User
from backend.models.blocked_token import BlockedToken

def register_jwt_loaders(jwt, db):
    # 保護されたエンドポイントにアクセスしようとしたが、有効なJWTが提供されなかった場合に呼び出されます
    # （例: Authorizationヘッダーがない、または形式が不正（例: "Bearer "が欠けている）な場合）。
    @jwt.unauthorized_loader
    def unauthorized_response(error_message):
        raise Unauthorized("Authorization header is missing or malformed. Please provide a valid JWT.")


    # Authorizationヘッダーは存在するものの、提供されたJWTが無効な場合
    # （例: 署名が不正、JWTの構造が壊れている、不正な形式のデータが埋め込まれている）
    @jwt.invalid_token_loader
    def invalid_token_response(error_message):
        raise Unauthorized("The provided token is invalid or its signature could not be verified.")


    # トークンの有効期限（expクレーム）が切れている場合に呼び出されます。
    @jwt.expired_token_loader
    def token_expires_callback(jwt_header, jwt_payload):
        raise Unauthorized("The provided token has expired. Please log in again.")


    # トークンが有効で期限切れでもないが、ブラックリストに登録され失効済みである場合に呼び出されます。
    # このローダーがTrueを返すと、必ずrevoked_token_loaderが呼び出されます。
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        stmt = select(BlockedToken).where(BlockedToken.jti == jti)
        blocked_token = db.session.execute(stmt).scalar_one_or_none()
        if blocked_token:
            return True
        return False


    # 現在のトークン（jwt_data["jti"] で識別される）がブロックリストに含まれているかをチェックします。
    @jwt.revoked_token_loader
    def revoked_token_response(jwt_header, jwt_payload):
        raise Unauthorized("This token has been revoked. Please obtain a new one.")


    # JWTのサブジェクト（通常はユーザーID）からユーザーオブジェクトをロードするために使用されます。
    # ユーザーが存在しない場合や無効な場合はNoneを返す必要があります。
    # このローダーがNoneを返すと、User not foundエラーになります。
    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_payload):
        user_id = jwt_payload['sub']
        return db.session.get(User, user_id)


    @jwt.user_lookup_error_loader
    def user_lookup_error(jwt_header, jwt_payload):
        raise Unauthorized("User associated with this token was not found.")