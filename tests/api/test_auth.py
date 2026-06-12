from tabnanny import check
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

    @allure.title("Тест регистрации пользователя с помощью Mock")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Ivan Petrovich")
    def test_register_user_mock(self, api_manager: ApiManager, test_user, mocker):
        with allure.step(" Мокаем метод register_user в auth_api"):
            mock_response = RegisterUserResponse(  # Фиктивный ответ
                id="id",
                email="email@email.com",
                fullName="fullName",
                verified=True,
                banned=False,
                roles=[Roles.SUPER_ADMIN],
                createdAt=str(datetime.datetime.now())
            )

            mocker.patch.object(
                api_manager.auth_api,  # Объект, который нужно замокать
                'register_user',  # Метод, который нужно замокать
                return_value=mock_response  # Фиктивный ответ
            )

        with allure.step("Вызываем метод, который должен быть замокан"):
            register_user_response = api_manager.auth_api.register_user(test_user)

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with allure.step("Проверка поля персональных данных"):  # обратите внимание на вложенность allure.step
                with check:
                    # Строка ниже выдаст исклющение и но выполнение теста продолжится
                    check.equal(register_user_response.fullName, "INCORRECT_NAME", "НЕСОВПАДЕНИЕ fullName")
                    check.equal(register_user_response.email, mock_response.email)

            with allure.step("Проверка поля banned"):
                with check("Проверка поля banned"):  # можно использовать вместо allure.step
                    check.equal(register_user_response.banned, mock_response.banned)
