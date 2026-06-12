import requests
from faker import Faker
from constants.constants import BASE_URL, REGISTER_ENDPOINT
from api.api_manager import ApiManager
import pytest
from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helper import DBHelper
from models.basic_models import TestUser

faker = Faker()

@pytest.fixture
def test_user() -> TestUser:
    """Возвращает объект TestUser"""
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

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
def movie_id(super_admin):
    movie = super_admin.api.movie_api.create_movie({
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
    super_admin.api.movie_api.delete_movie(movie_id)

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

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        list(Roles.SUPER_ADMIN.value),
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.ADMIN.value),
        new_session)
    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope='function')
def created_movie_data(db_helper):
    movie = db_helper.create_movie(DataGenerator.generate_movie_data())
    yield movie
    if db_helper.get_movie_by_id(movie.id):
        db_helper.delete_movie(movie)
        
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

