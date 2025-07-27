import uuid
from flask import url_for
from backend.models.user import User

# --- GET /admin/users ---
class TestGetUserlist:
    def test_get_userlist_success(self, client, authenticated_admin, db):
        """
        正常系: 管理者がユーザーリストを正常に取得できる
        """
        # テスト用の一般ユーザーを複数作成
        db.session.add(User(username='user1', email='u1@example.com', password='p'))
        db.session.add(User(username='user2', email='u2@example.com', password='p'))
        db.session.commit()

        admin_user, access_token = authenticated_admin
        headers = {'Authorization': f'Bearer {access_token}'}

        response = client.get(url_for('admin.get_userlist'), headers=headers)
        data = response.get_json()

        assert response.status_code == 200
        # ユーザーリストの長さで確認 (管理者自身 + 作成した2人 = 3人)
        assert len(data['users']) == 3

    def test_get_userlist_by_non_admin(self, client, authenticated_user):
        """
        異常系: 非管理者ユーザーがアクセスすると403 Forbidden
        """
        user, access_token = authenticated_user # 非管理者ユーザー
        headers = {'Authorization': f'Bearer {access_token}'}

        response = client.get(url_for('admin.get_userlist'), headers=headers)
        data = response.get_json()

        assert response.status_code == 403
        assert data['error_code'] == 'FORBIDDEN'


# --- PATCH /admin/users/<user_id>/change-role ---
class TestChangeRole:
    def test_change_role_success(self, client, authenticated_admin, db):
        """
        正常系: 管理者がユーザーの役割を変更できる
        """
        # 役割を変更されるユーザーを作成
        user_to_change = User(username='regular_user', email='ru@example.com', password='p', is_admin=False)
        db.session.add(user_to_change)
        db.session.commit()
        assert user_to_change.is_admin is False

        admin_user, access_token = authenticated_admin
        headers = {'Authorization': f'Bearer {access_token}'}

        url = url_for('admin.change_role', user_id=user_to_change.id)
        response = client.patch(url, headers=headers)

        assert response.status_code == 200

        # DBで役割が変更されたことを確認
        db.session.refresh(user_to_change)
        assert user_to_change.is_admin is True

    def test_change_role_user_not_found(self, client, authenticated_admin):
        """
        異常系: 存在しないユーザーの役割を変更しようとすると404エラー
        (注: view関数が正しく修正された後の期待される挙動)
        """
        non_existent_id = uuid.uuid4()
        admin_user, access_token = authenticated_admin
        headers = {'Authorization': f'Bearer {access_token}'}

        url = url_for('admin.change_role', user_id=non_existent_id)
        response = client.patch(url, headers=headers)
        data = response.get_json()

        # 期待するステータスコードを500から404に変更
        assert response.status_code == 404
        assert data['error_code'] == 'NOT_FOUND'


# --- DELETE /admin/users/<user_id>/delete-user ---
class TestAdminDeleteUser:
    def test_delete_user_success(self, client, authenticated_admin, db):
        """
        正常系: 管理者が指定したユーザーを削除できる
        """
        # 削除されるユーザーを作成
        user_to_delete = User(username='delete_me', email='dm@example.com', password='p')
        db.session.add(user_to_delete)
        db.session.commit()
        user_id = user_to_delete.id

        admin_user, access_token = authenticated_admin
        headers = {'Authorization': f'Bearer {access_token}'}

        url = url_for('admin.delete_user', user_id=user_id)
        response = client.delete(url, headers=headers)

        assert response.status_code == 204 # No Content

        # DBからユーザーが削除されたことを確認
        deleted_user = db.session.get(User, user_id)
        assert deleted_user is None

    def test_delete_user_by_non_admin(self, client, authenticated_user, db):
        """
        異常系: 非管理者ユーザーが削除しようとすると403 Forbidden
        """
        # 削除対象のユーザー
        target_user = User(username='target', email='target@example.com', password='p')
        db.session.add(target_user)
        db.session.commit()

        user, access_token = authenticated_user # 非管理者
        headers = {'Authorization': f'Bearer {access_token}'}

        url = url_for('admin.delete_user', user_id=target_user.id)
        response = client.delete(url, headers=headers)
        data = response.get_json()

        assert response.status_code == 403
        assert data['error_code'] == 'FORBIDDEN'

    def test_delete_user_not_found(self, client, authenticated_admin):
        """
        異常系: 存在しないユーザーを削除しようとすると404 Not Found
        """
        non_existent_id = uuid.uuid4()
        admin_user, access_token = authenticated_admin
        headers = {'Authorization': f'Bearer {access_token}'}

        url = url_for('admin.delete_user', user_id=non_existent_id)
        response = client.delete(url, headers=headers)
        data = response.get_json()

        assert response.status_code == 404
        assert data['error_code'] == 'NOT_FOUND'