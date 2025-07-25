
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

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=3)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=5)

    # Trueに設定すると、クッキーを利用した際のクロスサイトリクエストフォージェリ（CSRF）保護が有効になります。
    JWT_COOKIE_CSRF_PROTECT = False

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

class ProductionConfig(BaseConfig):
    # Trueに設定すると、クッキーはHTTPS経由でのみ送信されるようになります。
    JWT_REFRESH_COOKIE_SECURE = True

