'''
class TestUser:

    def test_create_user(self, super_admin, created_test_user):
        response = super_admin.api.user_api.create_user(created_test_user).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == created_test_user['email']
        assert response.get('fullName') == created_test_user['fullName']
        assert response.get('roles', []) == created_test_user['roles']
        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, created_test_user):
        created_user_response = super_admin.api.user_api.create_user(created_test_user).json()
        response_by_id = super_admin.api.user_api.get_user(created_test_user['id']).json()
        response_by_email = super_admin.api.user_api.get_user(created_test_user['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == created_test_user['email']
        assert response_by_id.get('fullName') == created_test_user['fullName']
        assert response_by_id.get('roles', []) == created_test_user['roles']
        assert response_by_id.get('verified') is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
'''