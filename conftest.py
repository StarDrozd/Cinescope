import requests
from faker import Faker
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from api.api_manager import ApiManager
import pytest
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
faker = Faker()

@pytest.fixture()
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture
def registered_user():
    user_data = {
        "email": "unique_email@mail.com",
        "fullName": 'Mr Uniqueness Unique',
        "password": 'Unique_password12345',
        "passwordRepeat": 'Unique_password12345'
    }
    requests.post(f'{BASE_URL}{REGISTER_ENDPOINT}', json=user_data)
    return {'email': user_data['email'],
            'password': user_data['password']
            }

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)