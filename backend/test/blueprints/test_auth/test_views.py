from flask import url_for, current_app # current_app をインポート
from backend.models.user import User
from backend.models.blocked_token import BlockedToken

# ... (TestRegistrationクラスはそのまま) ...


# --- POST /auth/login ---
class TestLogin:
    def setup_method(self, method):
        # 各テストの前に実行されるセットアップ
        self.test_user_email = 'test@example.com'
        self.test_user_password = 'Password123!'

    def test_login_success(self, client, db):
        """
        正常系: 正しい認証情報でログインできる
        """
        # ... (ユーザー作成部分はそのまま) ...
        u = User(username='testuser', email=self.test_user_email)
        u.set_password_hash(self.test_user_password)
        db.session.add(u)
        db.session.commit()

        payload = {'email': self.test_user_email, 'password': self.test_user_password}
        response = client.post(url_for('auth.login'), json=payload)
        data = response.get_json()

        assert response.status_code == 200
        assert 'access_token' in data
        assert data['user']['email'] == self.test_user_email

        # --- ↓↓↓ ここを修正！ ↓↓↓ ---
        # アプリケーションの設定から正しいクッキー名を取得してアサートする
        cookie_name = current_app.config['JWT_REFRESH_COOKIE_NAME']
        assert cookie_name in response.headers.get('Set-Cookie')
        # --- ↑↑↑ ここを修正！ ↑↑↑ ---

    # ... (test_login_wrong_credentials はそのまま) ...
    def test_login_wrong_credentials(self, client, db):
        u = User(username='testuser', email=self.test_user_email)
        u.set_password_hash(self.test_user_password)
        db.session.add(u)
        db.session.commit()
        payload = {'email': self.test_user_email, 'password': 'wrong_password'}
        response = client.post(url_for('auth.login'), json=payload)
        data = response.get_json()
        assert response.status_code == 401
        assert data['error_code'] == 'UNAUTHORIZED'


# --- POST /auth/logout & /auth/refresh-tokens ---
class TestTokenFlow:
    # --- ↓↓↓ ここからが修正部分 ↓↓↓ ---
    # このクラス内のすべてのテストで、正しいクッキー名を使うように修正
    # （このクラスには修正は不要ですが、もしあれば同様に行います）
    # このテストの失敗は、`TestLogin`のクッキー名の不一致が原因で、
    # そもそもリフレッシュトークンが正しくセットされなかったことに起因します。
    # 上記の`TestLogin`の修正だけで、こちらのテストもパスするはずです。
    # --- ↑↑↑ ここまでが修正部分 ↑↑↑ ---
    def test_logout_and_refresh_flow(self, client, db):
        """
        正常系: ログイン、リフレッシュ、ログアウトの一連の流れをテスト
        """
        # ... (1. と 2. のステップはそのまま) ...
        # 1. ユーザーを作成し、ログインしてトークンを取得
        email, password = 'flow@example.com', 'Password123!'
        u = User(username='flowuser', email=email)
        u.set_password_hash(password)
        db.session.add(u)
        db.session.commit()

        login_payload = {'email': email, 'password': password}
        login_response = client.post(url_for('auth.login'), json=login_payload)
        assert login_response.status_code == 200

        # 2. リフレッシュトークンを使ってアクセストークンを再発行
        refresh_response = client.post(url_for('auth.refresh_tokens'))
        refresh_data = refresh_response.get_json()
        assert refresh_response.status_code == 200
        assert 'access_token' in refresh_data
        assert BlockedToken.query.count() == 1

        # 3. 新しいリフレッシュトークンを使ってログアウト
        logout_response = client.post(url_for('auth.logout'))
        assert logout_response.status_code == 200

        # ログアウトしたリフレッシュトークンもブロックされたか確認
        assert BlockedToken.query.count() == 2

        # --- ↓↓↓ ここを修正！ ↓↓↓ ---
        # クッキーを削除するヘッダーがあるか確認 (Expiresが設定されているかでチェック)
        assert 'Expires=' in logout_response.headers.get('Set-Cookie')
        # --- ↑↑↑ ここを修正！ ↑↑↑ ---

        # 4. (おまけ) ブロックされたリフレッシュトークンで再度リフレッシュを試みる
        final_refresh_response = client.post(url_for('auth.refresh_tokens'))
        final_refresh_data = final_refresh_response.get_json()
        assert final_refresh_response.status_code == 401
        assert final_refresh_data['error_code'] == 'AUTHORIZATION_HEADER_MISSING'