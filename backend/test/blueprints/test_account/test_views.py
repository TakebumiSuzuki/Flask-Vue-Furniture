from flask import url_for
from backend.models.user import User


# --- GET /account ---
class TestGetUser:
    def test_get_user_success(self, client, authenticated_user):
        """
        正常系: 認証済みユーザーが自身の情報を取得できる
        """
        user, access_token = authenticated_user
        headers = {'Authorization': f'Bearer {access_token}'}

        response = client.get(url_for('account.get_user'), headers=headers)
        data = response.get_json()

        assert response.status_code == 200
        assert data['user']['username'] == user.username
        assert data['user']['email'] == user.email
        assert 'password' not in data['user'] # パスワードが含まれていないことを確認

    def test_get_user_unauthorized(self, client):
        """
        異常系: 認証なしでアクセスした場合、401エラーが返る
        """
        response = client.get(url_for('account.get_user'))
        data = response.get_json()

        assert response.status_code == 401
        assert data['error_code'] == 'AUTHORIZATION_HEADER_MISSING'



# --- DELETE /account ---
class TestDeleteUser:
    def test_delete_user_success(self, client, authenticated_user, db):
        """
        正常系: 認証済みユーザーが自身のアカウントを削除できる
        """
        user, access_token = authenticated_user
        headers = {'Authorization': f'Bearer {access_token}'}

        response = client.delete(url_for('account.delete_user'), headers=headers)
        data = response.get_json()

        assert response.status_code == 200
        assert data['message'] == 'Account deleted successfully.'

        # DBからユーザーが削除されたことを確認
        deleted_user = db.session.get(User, user.id)
        assert deleted_user is None

    def test_delete_user_unauthorized(self, client):
        """
        異常系: 認証なしでアクセスした場合、401エラーが返る
        """
        response = client.delete(url_for('account.delete_user'))
        data = response.get_json()

        assert response.status_code == 401
        assert data['error_code'] == 'AUTHORIZATION_HEADER_MISSING'


# --- PATCH /account/update-username ---
class TestUpdateUsername:
    def test_update_username_success(self, client, authenticated_user, db):
        """
        正常系: ユーザー名を正常に変更できる
        """
        user, access_token = authenticated_user
        headers = {'Authorization': f'Bearer {access_token}'}
        payload = {'username': 'new_username'}

        response = client.patch(url_for('account.username_change'), headers=headers, json=payload)

        assert response.status_code == 200

        # DBでユーザー名が変更されたことを確認
        db.session.refresh(user)
        assert user.username == 'new_username'

    def test_update_username_conflict(self, client, authenticated_user, db):
        """
        異常系: 既に使用されているユーザー名に変更しようとすると409エラー
        """
        # 別のユーザーをあらかじめ作成しておく
        other_user = User(username='existing_user', email='other@example.com')
        other_user.set_password_hash('Password123!')
        db.session.add(other_user)
        db.session.commit()

        user, access_token = authenticated_user
        headers = {'Authorization': f'Bearer {access_token}'}
        payload = {'username': 'existing_user'} # 既存のユーザー名

        response = client.patch(url_for('account.username_change'), headers=headers, json=payload)
        data = response.get_json()

        assert response.status_code == 409
        assert data['error_code'] == 'CONFLICT'
        assert data['message'] == 'This username already exists.'

    def test_update_username_validation_error(self, client, authenticated_user):
        """
        異常系: バリデーションに失敗する短いユーザー名を送信すると422エラー
        """
        user, access_token = authenticated_user
        headers = {'Authorization': f'Bearer {access_token}'}
        payload = {'username': 'a'} #短すぎるユーザー名

        response = client.patch(url_for('account.username_change'), headers=headers, json=payload)
        data = response.get_json()

        assert response.status_code == 422
        assert data['error_code'] == 'VALIDATION_ERROR'


# --- PATCH /account/update-password ---
class TestUpdatePassword:
    def test_update_password_success(self, client, authenticated_user, db):
        """
        正常系: パスワードを正常に変更できる
        """
        user, access_token = authenticated_user
        headers = {'Authorization': f'Bearer {access_token}'}
        payload = {
            'old_password': 'Password123!',
            'new_password': 'NewPassword456!' # 要件を満たす新しいパスワード
        }

        response = client.patch(url_for('account.password_update'), headers=headers, json=payload)

        assert response.status_code == 200

        # DBでパスワードが変更されたことを確認
        db.session.refresh(user)
        assert user.check_password_match('NewPassword456!')
        assert not user.check_password_match('Password123!') # 古いパスワードでは認証できない

    def test_update_password_wrong_old_password(self, client, authenticated_user):
        """
        異常系: 古いパスワードが間違っている場合、401エラー
        """
        user, access_token = authenticated_user
        headers = {'Authorization': f'Bearer {access_token}'}
        payload = {
            'old_password': 'WRONG_PASSWORD',
            'new_password': 'NewPassword456!'
        }

        response = client.patch(url_for('account.password_update'), headers=headers, json=payload)
        data = response.get_json()

        assert response.status_code == 401
        assert data['error_code'] == 'UNAUTHORIZED'
        assert data['message'] == 'Old password is not correct.'

    def test_update_password_validation_error(self, client, authenticated_user):
        """
        異常系: 新しいパスワードが要件を満たさない場合、422エラー
        """
        user, access_token = authenticated_user
        headers = {'Authorization': f'Bearer {access_token}'}
        payload = {
            'old_password': 'Password123!',
            'new_password': 'weak' # 要件を満たさないパスワード
        }

        response = client.patch(url_for('account.password_update'), headers=headers, json=payload)
        data = response.get_json()

        assert response.status_code == 422
        assert data['error_code'] == 'VALIDATION_ERROR'