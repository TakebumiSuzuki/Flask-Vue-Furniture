import os
import logging
from flask import Flask
from flask_cors import CORS

from backend.config import DevelopmentConfig, ProductionConfig
from backend.extensions import db, jwt, migrate
from backend.jwt_loaders import register_jwt_loaders
from backend.errors import register_error_handlers
from backend.blueprints.admin.views import admin_bp
from backend.blueprints.auth.views import auth_bp
from backend.blueprints.account.views import account_bp


def create_app(config_override=None) -> Flask:

    if config_override: #テスト用
        # pytestでテストを実行する際にはflask runを使わないので、環境変数FLASK_DEBUGは関係ない。
        # app.config['TESTING'] = True と app.config['DEBUG'] = False にすることが重要。
        config = config_override

    else: # flask run 用
        print(f"デバックの数字： {os.getenv("FLASK_DEBUG", "0")}")
        debug_flag = os.getenv("FLASK_DEBUG", "0") in ("1", "true", "True")
        config = DevelopmentConfig if debug_flag else ProductionConfig

    app = Flask(__name__)
    app.config.from_object(config)

    level = logging.DEBUG if app.config.get("DEBUG", False) else logging.INFO
    app.logger.setLevel(level)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_error_handlers(app, db)
    register_jwt_loaders(jwt, db)

    CORS(
        app,
        origins=app.config.get("CORS_ORIGINS", ["http://localhost:5173"]),
        supports_credentials=True,
    )

    app.register_blueprint(admin_bp,   url_prefix="/api/v1/admin")
    app.register_blueprint(auth_bp,    url_prefix="/api/v1/auth")
    app.register_blueprint(account_bp, url_prefix="/api/v1/account")

    # --- デバッグ用の情報表示 ---
    # デバッグモードが有効な場合のみ、URL一覧を表示する
    if app.config.get("DEBUG"):
        with app.app_context():
            print("--- REGISTERED URLS ---")
            for rule in app.url_map.iter_rules():
                print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, URL: {rule.rule}")
            print("-----------------------")

    return app

# `python -m flask run` と `flask run` は、開発サーバーを起動するほぼ同じコマンド。
# どちらの場合も、まず環境変数 `FLASK_APP` による指定を最優先で探します。
# `FLASK_APP`環境変数が設定されてない場合に、規約に従ってカレントディレクトリの `app.py` または `wsgi.py` を探します。
# Flaskはカレントディレクトリに app.py または wsgi.py という名前のファイルがあるかを探し、あれば実行する。
# 発見したファイルの中では、以下の優先順位でアプリケーションを特定します。
# 1. (最優先) `create_app` または `make_app` という名前のファクトリ関数。
#    → 見つかれば、この関数を【引数なしで】呼び出し、その戻り値をアプリとして使用します。
# 2. (上記がない場合) `app` という名前のFlaskインスタンスのグローバル変数。

# flask runをして起動される開発サーバーはただ一つのappを密結合として保持する。
# そしてリクエストがあると、サーバーはappに対してそのリクエスを渡す。appは登録されているルーティングの
# view関数を実行するが、その前に、コンテキストスタックを準備する。なぜならばdbや他のパッケージは
# コンテキストスタックの最後にプッシュされた app　への参照を使うから。そしてview関数の実行が終わると
# このコンテキストスタックからプッシュされたappはpopされて消える
# Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Migrate, Flask-Loginなど、
# 適切に設計されたほぼ全てのFlask拡張機能は、この規約に従っています。



if __name__ == "__main__": # 直接 `python app.py` で動かすとき
    flask_app = create_app()
    flask_app.run(
        host="0.0.0.0",
        debug=flask_app.config.get("DEBUG", False),
    )
