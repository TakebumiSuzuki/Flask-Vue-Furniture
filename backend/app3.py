# docker build -t flask-app-test .
# docker run --rm -p 5001:5000 -v "$(pwd)/:/app/" -e FLASK_DEBUG=1 flask-app-test

import logging
from flask import Flask
from flask_cors import CORS
from backend.extensions import db, jwt, migrate
from backend.config import DevelopmentConfig, ProductionConfig
from backend.blueprints.admin.views import admin_bp
from backend.blueprints.auth.views import auth_bp
from backend.blueprints.account.views import account_bp
from backend.jwt_loaders import register_jwt_loaders
from backend.errors import register_error_handlers

app = Flask(__name__)
# from_object は渡されたオブジェクト（クラスでもインスタンスでも）が持つ、名前がすべて大文字の属性を探し出し、
# それらを app.config にキーと値としてコピーする。DevelopmentConfig()としてもオッケー。
app.config.from_object(DevelopmentConfig)
app.logger.setLevel(logging.DEBUG)

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
register_error_handlers(app, db)
register_jwt_loaders(jwt, db)


# originsの設定により、Flaskサーバーは、ブラウザに対して「http://localhost:5173 からのリクエストは安全だから
# 許可していいですよ」という特別なヘッダー (Access-Control-Allow-Origin) を返す。
# supports_credentialsを Trueにすると、Flaskサーバーは「このサーバーとの通信ではCookieや HTTPのAuthorizationヘッダー
# のやり取りを許可します」というヘッダー (Access-Control-Allow-Credentials: true) を返します。
# フロントエンド（axios）側のリクエスト設定 withCredentials: true と必ずセットで使わないと意味がない。
CORS(
    app,
    origins=["http://localhost:5173"],
    supports_credentials=True
)


# register_error_handlers(app)
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(account_bp, url_prefix='/api/v1/account')

# ルートURL ("/") にアクセスがあった場合の処理
@app.route('/')
def hello_world():
    return '<h1>jjフfeafaaa</h1>'

with app.app_context():
    print("--- REGISTERED URLS ---")
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, URL: {rule.rule}")
    print("-----------------------")

# (docker run でコマンドを指定するので、実際にはこちらは使われないが、
# ローカルで直接 python app.py と実行してテストする際に便利)
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)