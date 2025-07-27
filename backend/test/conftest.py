
# テスト実行は
# docker-compose run --rm backend sh -c "pip install -r requirements-dev.txt && pytest"

import sys, os
# プロジェクトのルートディレクトリ(/backend)の、さらに親('/)を検索パスに追加する
# これにより、'from backend.app'というインポートが可能になる
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from backend.app import create_app
from backend.extensions import db as _db  # 関数名のdbと名前の衝突が起こらないようにするため
from backend.config import TestingConfig
from flask_jwt_extended import create_access_token
from backend.models.user import User

@pytest.fixture(scope='session')
def app():
    app = create_app(config_override=TestingConfig)

    with app.app_context():
        yield app
    # 上の部分はこの場合、return appでも問題ないが、yield appとすることで、将来、必要ならば後片付けのコードを追加することが可能
    # cleanup_temporary_files()


@pytest.fixture(scope='session')
def client(app):
    # test_client()は、Flaskのアプリケーションオブジェクト (app) に、テスト目的のためにデフォルトで用意されているメソッド。
    # 実際のネットワーク通信を発生させることなく、あなたのFlaskアプリケーションに対してHTTPリクエストをシミュレートできる、
    # 「プログラムで操作できる、擬似的なWebブラウザ」のように振る舞う。
    return app.test_client()


# @pytest.fixture で修飾された db(app) 関数は、Pythonの文法上、ジェネレータ関数と考えて良い。
@pytest.fixture(scope='function', autouse=True)
def db(app): # db_fixtureという名前に変えてもOK
    """
    各テスト関数の実行前にデータベースをクリーンな状態にし、
    実行後に後片付けを行います。
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all() # 全テーブルを削除


@pytest.fixture(scope='function')
def authenticated_user(db):
    """
    テスト用の認証済みユーザーを作成し、
    ユーザーオブジェクトとアクセストークンを返します。
    """
    # テスト用のユーザーをDBに作成
    user = User(username='testuser', email='test@example.com')
    user.set_password_hash('Password123!') # スキーマの要件を満たすパスワード
    db.session.add(user)
    db.session.commit()

    # そのユーザーのアクセストークンを生成
    access_token = create_access_token(identity=user.id)

    return user, access_token


@pytest.fixture(scope='function')
def authenticated_admin(db):
    """
    テスト用の認証済み「管理者」ユーザーを作成し、
    ユーザーオブジェクトとアクセストークンを返します。
    """
    # is_admin=True で管理者ユーザーをDBに作成
    admin_user = User(username='adminuser', email='admin@example.com', is_admin=True)
    admin_user.set_password_hash('Password123!')
    db.session.add(admin_user)
    db.session.commit()

    # その管理者ユーザーのアクセストークンを生成
    access_token = create_access_token(identity=admin_user.id)

    return admin_user, access_token





# pytest を実行すると、カレントディレクトリ（またはコマンドで指定されたパス）から、下に向かって再帰的に
# （つまり、サブディレクトリの中へ中へと）探索を開始します。

# 探索の過程で、pytestは各ディレクトリにある conftest.py という名前のファイルを見つけ、読み込みます。
# そして、そこに定義されているフィクスチャやフック（pytestの動作をカスタマイズする関数）は、それ以下のすべての
# サブディレクトリ内にあるテストで利用可能になります。

# 探索中、pytestは標準で以下の命名規則に一致するファイルを探します。
# test_*.py （test_ で始まるファイル）または、
# *_test.py （_test で終わるファイル）

# 発見したテストファイルの中で、さらに以下のものをテストとして認識します。
# test_ で始まる名前の関数（例: def test_login():）
# Test で始まる名前のクラスの中にある、test_ で始まる名前のメソッド（例: class TestAuth: def test_login(self):）

# すべてのテスト対象を「収集（Collection）」し終えた後、pytestはそれらを順番に実行していきます。
