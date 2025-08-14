
import os
from datetime import timedelta

class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # この値が設定されていない場合は、FlaskのSECRET_KEYが代わりに使用されます。
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ERROR_MESSAGE_KEY = 'message'

    # 複数の場所を指定することもでき、その場合はリストの順序で優先的に検索されます。
    JWT_TOKEN_LOCATION = ['headers', 'cookies']

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)

    # Trueに設定すると、クッキーを利用した際のクロスサイトリクエストフォージェリ（CSRF）保護が有効になります。
    # @jwt_required() デコレーターで保護されており、かつ locations=["cookies"] が指定されている
    # エンドポイントでのみ X-CSRF-TOKEN ヘッダーの検証が行われる
    JWT_COOKIE_CSRF_PROTECT = True

    # リフレッシュトークンのクッキーが有効なパスを指定しエンドポイントを限定できます。
    # が、リストを設定できない、つまり一つのパスしか指定できないので、ここでは設定しない
    # JWT_REFRESH_COOKIE_PATH =

    JWT_REFRESH_COOKIE_NAME = 'refresh_token_furniture_site'
    JWT_REFRESH_COOKIE_SAMESITE = 'Lax'
# .envなどを使い、環境変数にFLASK_DEBUG=1を設定すると、Flaskはアプリケーションを「デバッグモード」で起動します。
# これには、インタラクティブデバッガの有効化や、コード変更時の自動リローダーの起動が含まれます。
# そして、さらに同時に、Flaskが内部的にapp.config['DEBUG']をTrueに設定する(ここでの設定を上書きする)
# 結論として、Configの中にはDEBUGを書く必要はない。


class DevelopmentConfig(BaseConfig):
    # Trueに設定すると、クッキーはHTTPS経由でのみ送信されるようになります。
    JWT_REFRESH_COOKIE_SECURE = False
    PROPAGATE_EXCEPTIONS = True

class ProductionConfig(BaseConfig):
    # Trueに設定すると、クッキーはHTTPS経由でのみ送信されるようになります。
    JWT_REFRESH_COOKIE_SECURE = True


class TestingConfig(BaseConfig):
    # TESTING は、Flaskフレームワーク自体によって認識される、デフォルトで定義済みの特別な設定キー
    # これにより、エラーハンドラはエラーをキャッチせず、発生した例外をそのまま上位に伝播させ、
    # pytest のようなテストフレームワークがその例外を直接捕捉し、「期待したエラーが発生したか」を検証できるようにする。
    # このほかにもいくつか同時に設定が変わる
    TESTING = True

    # テストではインタラクティブデバッガ（ブラウザ上のエラー画面),コード変更時の自動リロードなどは不要なのでFalseに。
    # これがFalseであることで、テストはノイズのないクリーンな環境で、効率的に実行されます。強く推奨される設定です。
    # DEBUG = Trueだと、アプリケーションでエラーが発生すると、Werkzeugのインタラクティブデバッガーが例外を「キャッチ」
    # してしまい、テストフレームワーク側は「エラーが発生した」という事実を検知できなくなります。
    DEBUG = False

    # テスト中は、リフレッシュトークンのクッキーに対するCSRF保護を無効にする
    JWT_COOKIE_CSRF_PROTECT = False


    # Pythonの標準ライブラリに最初から組み込まれている sqlite3 モジュールが使われる。
    # で、このモジュールはpythonをダウンロードした時にバンドルされているsqliteを必ず使う。
    # SQLAlchemyはこのsqlite3モジュールを呼び出し、データベースへの接続を確立するように指示します
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL",
        "sqlite:///:memory:"
    )

