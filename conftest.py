import requests
from faker import Faker
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from api.api_manager import ApiManager
import pytest
from utils.data_generator import DataGenerator
faker = Faker()

@pytest.fixture
def admin_auth(api_manager):
    """Авторизация администратора."""
    admin_creds = ('api1@gmail.com', 'asdqwe123Q')
    api_manager.auth_api.authenticate(admin_creds)
    yield api_manager

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
@pytest.fixture(scope='function')
def new_movie_data():
    return {
        "name": f'About {faker.first_name()} + {faker.last_name()}',
        "imageUrl": "https://example.com/image.png",
        "price": 100,
        "description": f'Absolute cinema about {faker.date()} years and {faker.last_name()}',
        "location": "SPB",
        "published": True,
        "genreId": 1
    }

@pytest.fixture
def updated_movie_data():
    return {
  "name": f"{faker.name()}",
  "description": f"Movie about {faker.first_name()}",
  "price": 100,
  "location": "SPB",
  "imageUrl": "https://image.url",
  "published": True,
  "genreId": faker.random_int(min=1, max=11)
}

@pytest.fixture()
def invalid_movie_data():
    return {
        'name': 'invalid',
        'price': 'invalidprice'
    }

@pytest.fixture()
def movie_id(admin_auth):
    movie = admin_auth.movie_api.create_movie({
        "name": faker.catch_phrase(),
        "imageUrl": "https://example.com/image.png",
        "price": 100,
        "description": "The story about..",
        "location": "SPB",
        "published": True,
        "genreId": 1
    })
    movie_id = movie.json()['id']
    yield movie_id
    admin_auth.movie_api.delete_movie(movie_id)

@pytest.fixture()
def get_params():
    params = {
        "pageSize": faker.random_int(min=1, max=5),
        "page": faker.random_int(min=1, max=3),
        "minPrice": faker.random_int(min=1, max=1000),
        "maxPrice": faker.random_int(min=1001, max=2000),
        "locations": faker.random_element(['SPB', 'MSK']),
        "published": faker.random_element([True, False]),
        "genreId": faker.random_int(min=1, max=3),
        "createdAt": faker.random_element(['asc', 'desc']),
    }
    return params

@pytest.fixture(scope="function")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope='function')
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)