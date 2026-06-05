import pytest
import requests
from conftest import api_manager
from api.api_manager import ApiManager

class TestAuthAPI:
    def test_register_user(self, super_admin, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = super_admin.api.auth_api.register_user(test_user)
        response_data = response.json()

        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, common_user, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = common_user.api.auth_api.login_user(login_data,)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_get_user_info(self, super_admin, test_user):
        register_response = super_admin.api.auth_api.register_user(test_user)
        user_id = register_response.json()["id"]

        response = super_admin.api.user_api.get_user_info(user_id)

    def test_delete_user(self, super_admin, test_user):
        register_response = super_admin.api.auth_api.register_user(test_user)
        user_id = register_response.json()["id"]

        response = super_admin.api.user_api.delete_user(user_id)
