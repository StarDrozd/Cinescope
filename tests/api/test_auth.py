import allure
from constants.roles import Roles
from pytest_check import check
import pytest
import requests
from api.api_manager import ApiManager
from models.basic_models import RegisterUserResponse
import datetime

def test_check_functions():
    check.equal(1 + 1, 2, "Проверка сложения")
    check.not_equal(2 * 2, 5, "Проверка умножения")
    check.is_true(1 == 1, "Проверка истинности")
    check.is_in("hello", "hello world", "Проверка вхождения строки")

class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):

        response = api_manager.auth_api.register_user(user_data=test_user)
        register_user_response = RegisterUserResponse(**response.json())

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
