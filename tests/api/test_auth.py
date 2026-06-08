import pytest
import requests
from api.api_manager import ApiManager
from models.basic_models import RegisterUserResponse

class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        # Преобразуем объект в словарь прямо в тесте
        user_data = test_user.dict()

        response = api_manager.auth_api.register_user(user_data=user_data)
        register_user_response = RegisterUserResponse(**response.json())

        # test_user - объект, обращаемся через точку
        assert register_user_response.email == test_user.email, "Email не совпадает"
        assert register_user_response.fullName == test_user.fullName, "FullName не совпадает"

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
