from models.basic_models import FindOneMovieResponse, FindAllMoviesResponse, MovieResponse
import allure
import pytest
from conftest import movie_id, new_movie_data

@pytest.mark.api
class TestMoviesAPI:

    @pytest.mark.parametrize('param', [
    {"pageSize": 1, "minPrice": 1, "maxPrice": 1000, "locations": "SPB", "genreId": 3},
    {"pageSize": 17, "minPrice": 5, "maxPrice": 500, "locations": "MSK", "genreId": 2},
    {"pageSize": 13, "minPrice": 10, "maxPrice": 200, "locations": "SPB", "genreId": 3},
    ])
    def test_get_movies(self, common_user, param):
        with allure.step('Отправка get запроса с параметрами'):
            response = common_user.api.movie_api.get_movies(params=param)
            response_data = FindAllMoviesResponse(**response.json())

        with allure.step('Проверка количества фильмов на странице'):
            assert len(response_data.movies) <= params['pageSize']
            if response_data.movies:
                for movie in response_data.movies:
                    assert params['minPrice'] <= movie.price <= params['maxPrice']
                    assert movie.location == params['locations']
                    assert movie.genreId == params['genreId']

        with allure.step('Проверка количества страниц'):
            expected_pages = (response_data.count + params['pageSize'] - 1) // params['pageSize']
            assert response_data.pageCount == expected_pages

    def test_get_movie(self, common_user, movie_id):
        with allure.step('Отправка get запроса по movie_id'):
            response = common_user.api.movie_api.get_movie(movie_id)
            response_data = FindOneMovieResponse(**response.json())

        with allure.step('Проверка, что id фильма в ответа совпадает'):
            assert  response_data.id == movie_id

    def test_create_movie(self, super_admin, new_movie_data, db_helper):
        with allure.step('Отправка post запроса с авторизацией на создание фильма'):
            response = super_admin.api.movie_api.create_movie(new_movie_data)
            response_data = MovieResponse(**response.json())
            movie_id = response.json()['id']

        with allure.step('Проверки, что фильм создан с корректными данными'):
            assert response_data.name == new_movie_data['name']
            assert response_data.genreId == new_movie_data['genreId']
            assert response_data.published == new_movie_data['published']

        with allure.step('Проверка, что фильм создан после API запроса в бд'):
            movie_in_db = db_helper.get_movie_by_id(movie_id)
            assert movie_in_db is not None, 'Фильм не найден в БД'

    @pytest.mark.parametrize('movie_data', [{
        "name": 'Breaking bad: El-camino0',
        "imageUrl": "https://example.com/image.png",
        "price": 666,
        "description": 'testdesc',
        "location": "SPB",
        "published": True,
        "genreId": 3
    }])
    def test_delete_movie(self, super_admin, movie_data, db_helper):
        with allure.step('Отправка post запроса с авторизацией на создание фильма с параметрами'):
            create_movie = super_admin.api.movie_api.create_movie(movie_data)
            create_data = MovieResponse(**create_movie.json())
            movie_id = create_data.id

        with allure.step('Отправка delete запроса на удаление фильма по id, ранее созданного фильма'):
            response = super_admin.api.movie_api.delete_movie(movie_id)
            response_data = MovieResponse(**response.json())

        with allure.step('Проверка, что фильм действительно удален и его нельзя найти по тому же id'):
            checking = super_admin.api.movie_api.get_movie(movie_id, expected_status=404)
            assert checking.json()['message'] == 'Фильм не найден'

        with allure.step('Проверка, что фильм действительно удален в БД и его нельзя найти по тому же id'):
            movie_in_db = db_helper.get_movie_by_id(movie_id)
            assert movie_in_db is None, f"Фильм с id {movie_id} всё ещё существует в БД"

    def test_patch_movie(self, super_admin, movie_id, updated_movie_data):
        with allure.step('Отправка patch запроса на обновление данных о фильме'):
            response = super_admin.api.movie_api.patch_movie(movie_id, updated_movie_data)
            response_data = MovieResponse(**response.json())

        with allure.step('Проверки, что данные о фильме действительно обновились'):
            assert response_data.name == updated_movie_data['name']
            assert response_data.description == updated_movie_data['description']
            assert response_data.price == updated_movie_data['price']

@pytest.mark.api
@pytest.mark.negative
class TestNegativeMoviesAPI:
    def test_get_nonexistent_movie(self, common_user):
        with allure.step('Делаем несуществующий id и отправляем по нему get запрос'):
            movie_id =  88*14 * 37* 51  #делаем несуществующий айди
            response = common_user.api.movie_api.get_movie(movie_id, expected_status=404)

    @pytest.mark.parametrize('param', [{'pageSize': 1,
                                        "minPrice": 1,
                                        "maxPrice": 1000,
                                        "locations": 'SPB',
                                        "genreId": 3}])
    def test_create_conflict_movie(self, super_admin, param, new_movie_data):
        with allure.step('Ищем существующий фильм'):
            response = super_admin.api.movie_api.get_movies(params=param)
            movie_data = response.json()['movies'][0]
            movie_conflict_name = movie_data['name']
            new_movie_data['name'] = movie_conflict_name

        with allure.step('Отправка post запроса на создание фильма с конфликтными данными'):
            response = super_admin.api.movie_api.create_movie(new_movie_data, expected_status=409)
            response_data = response.json()

        with allure.step('Проверки тела ответа ожиданиям'):
            assert response_data['error'] == 'Conflict'
            assert response_data['message'] == "Фильм с таким названием уже существует"

    def test_create_movie_with_invalid_data(self, super_admin, invalid_movie_data):
        with allure.step('Отправка post запроса на создание фильма с неправильными данными'):
            response = super_admin.api.movie_api.create_movie(invalid_movie_data, expected_status=400)
            response_data = response.json()

        with allure.step('Проверка тела ответа ожиданиям'):
            assert response_data['error'] == "Bad Request"

    def test_create_movie_without_auth(self, common_user, new_movie_data):
        with allure.step('Отправка post запроса на создание фильма без авторизации'):
            response = common_user.api.movie_api.create_movie(new_movie_data, expected_status=403)

    def test_delete_movie_nonexistent_movie(self, super_admin):
        with allure.step('Отправка delete запроса на удаление фильма по несуществующему id'):
            movie_id = '31f013131'
            response = super_admin.api.movie_api.delete_movie(movie_id, expected_status=404)

    def test_delete_movie_without_auth(self, super_admin, common_user, new_movie_data):
        with allure.step('Отправка post запроса на создание фильма'):
            create_movie = super_admin.api.movie_api.create_movie(new_movie_data, expected_status=201)
            movie_id = create_movie.json()['id']

        with allure.step('Отправка delete запроса на удаление фильма без авторизации'):
            response = common_user.api.movie_api.delete_movie(movie_id, expected_status=403)

    def test_patch_movie_with_invalid_data(self, super_admin, invalid_movie_data, movie_id):
        with allure.step('Отправка patch запроса на обновление данных с некорректными данными'):
            response = super_admin.api.movie_api.patch_movie(movie_id, invalid_movie_data, expected_status=400)
