from flask import jsonify
from sqlalchemy import select
from backend.models.user import User
from backend.models.blocked_token import BlockedToken
from uuid import UUID

def register_jwt_loaders(jwt, db):
    # 保護されたエンドポイントにアクセスしようとしたが、有効なJWTが提供されなかった場合に呼び出されます
    # （例: Authorizationヘッダーがない、または形式が不正（例: "Bearer "が欠けている）な場合）。
    @jwt.unauthorized_loader
    def unauthorized_response(error_message):
        return jsonify({
            "message": "Authorization header is missing or malformed. Please provide a valid JWT.",
            "error_code": "AUTHORIZATION_HEADER_MISSING"
        }), 401


    # Authorizationヘッダーは存在するものの、提供されたJWTが無効な場合
    # （例: 署名が不正、JWTの構造が壊れている、不正な形式のデータが埋め込まれている）
    @jwt.invalid_token_loader
    def invalid_token_response(error_message):
        return jsonify({
            "message": "The provided token is invalid or its signature could not be verified.",
            "error_code": "INVALID_TOKEN"
        }), 401


    # トークンの有効期限（expクレーム）が切れている場合に呼び出されます。
    @jwt.expired_token_loader
    def token_expires_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "The provided token has expired. Please log in again.",
            "error_code": "TOKEN_EXPIRED"
        }), 401


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


    # トークンがブロックリストに含まれている場合に呼び出されます。（token_in_blocklist_loaderがTrueを返した場合）
    @jwt.revoked_token_loader
    def revoked_token_response(jwt_header, jwt_payload):
        return jsonify({
            "message": "This token has been revoked. Please obtain a new one.",
            "error_code": "TOKEN_REVOKED"
        }), 401


    # JWTのサブジェクト（通常はユーザーID）からユーザーオブジェクトをロードするために使用されます。
    # ユーザーが存在しない場合や無効な場合はNoneを返す必要があります。
    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_payload):
        user_id_str = jwt_payload['sub']
        user_id_uuid = UUID(user_id_str)
        return db.session.get(User, user_id_uuid)


    # user_lookup_loaderがNoneを返した場合に呼び出されます。
    @jwt.user_lookup_error_loader
    def user_lookup_error(jwt_header, jwt_payload):
        return jsonify({
            "message": "User associated with this token was not found.",
            "error_code": "USER_NOT_FOUND"
        }), 401


'''
エラー処理の階層
--------------------------------------------------
↑ 3. Werkzeugデバッガ (最終防衛ライン)
 |   - どの階層でも捕捉されなかった例外が、ここに届く
 |   - DEBUG=True の時だけ有効
--------------------------------------------------
↑ 2. Flaskアプリケーションのエラーハンドラ (`@app.errorhandler`)
 |   - アプリ全体で発生した例外を捕捉する「正規ルート」
 |   - raiseされた例外は、通常ここに届く
--------------------------------------------------
↑ 1. ライブラリ/デコレータの内部処理 (`@jwt_required`など)
 |   - View関数が実行される前に、ここで例外が発生することがある
--------------------------------------------------

と、いうことで、jwt-extendedで起きたエラーは、DEBUG = Falseの場合には @app.errorhandlerで補足可能なのだが。。。

DEBUG = True の場合 (意図的な迂回ルート)はjwt-extendedは特別な動作を行い、、
1. @jwt_required の中でエラーが発生し、あなたのローダーが raise Unauthorized します。
2. @jwt_required は、その例外を捕捉した瞬間に考えます。「今、DEBUGモードだ。 このエラーは、きっと開発者が原因を知りたいはずだ。正規ルートの @app.errorhandler に渡してJSONにしてしまうより、生の情報をデバッガで見せてあげよう。」
3.そこで、@jwt_requiredは、例外を上の階層に渡すことをやめて、わざと「捕捉されない例外」として**(3) Werkzeugデバッガ**に直接流します。
結果として、HTMLのデバッグ画面が表示されます。
つまり、Flaskアプリケーションのエラーハンドラをスキップしてしまう。
よって
[結論]
エラーのローダーで raise Unauthorized('') のように書くのではなく、jsonifyを使ってエラーのレスポンスを返すような実装にする。

'''