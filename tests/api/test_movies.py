import pytest
import requests
from conftest import admin_auth, movie_id
from api.api_manager import ApiManager

class TestMoviesAPI:
    def test_get_movies(self, common_user, get_params):
        response = common_user.api.movie_api.get_movies(params=get_params)
        response_data = response.json()

        assert response_data != {}
        assert response_data['movies'] != []
        assert type(response_data['movies']) is list
        assert len(response_data['movies']) <= get_params['pageSize']

    def test_get_movie(self, common_user, movie_id):
        response = common_user.api.movie_api.get_movie(movie_id)
        response_data = response.json()

        assert  response_data['id'] == movie_id

    def test_create_movie(self, super_admin, new_movie_data):
        response = super_admin.api.movie_api.create_movie(new_movie_data)
        response_data = response.json()

        assert response_data['name'] == new_movie_data['name']
        assert response_data['genreId'] == new_movie_data['genreId']
        assert response_data['published'] == new_movie_data['published']

    def test_delete_movie(self, super_admin, new_movie_data):
        create_movie = super_admin.api.movie_api.create_movie(new_movie_data)
        movie_id = create_movie.json()['id']

        super_admin.api.movie_api.delete_movie(movie_id)

        checking = super_admin.api.movie_api.get_movie(movie_id, expected_status=404)
        assert checking.json()['message'] == 'Фильм не найден'

    def test_patch_movie(self, super_admin, movie_id, new_movie_data, updated_movie_data):
        response = super_admin.api.movie_api.patch_movie(movie_id, updated_movie_data)

        assert response.json()['name'] == updated_movie_data['name']
        assert response.json()['description'] == updated_movie_data['description']
        assert response.json()['price'] == updated_movie_data['price']

class TestNegativeMoviesAPI:
    def test_get_nonexistent_movie(self, common_user):
        movie_id =  88*14 * 37* 51  #делаем несуществующий айди
        response = common_user.api.movie_api.get_movie(movie_id, expected_status=404)

    def test_create_conflict_movie(self, super_admin, new_movie_data):
        conflict_data = new_movie_data.copy()
        conflict_data['name'] = 'Название фильма'
        response = super_admin.api.movie_api.create_movie(conflict_data, expected_status=409)
        response_data = response.json()

        assert response_data['error'] == 'Conflict'
        assert response_data['message'] == "Фильм с таким названием уже существует"

    def test_create_movie_with_invalid_data(self, super_admin, invalid_movie_data):
        response = super_admin.api.movie_api.create_movie(invalid_movie_data, expected_status=400)
        response_data = response.json()

        assert response_data['error'] == "Bad Request"

    def test_create_movie_without_auth(self, common_user, new_movie_data):
        response = common_user.api.movie_api.create_movie(new_movie_data, expected_status=403)

    def test_delete_movie_nonexistent_movie(self, super_admin):
        movie_id = '31f013131'
        response = super_admin.api.movie_api.delete_movie(movie_id, expected_status=404)

    def test_delete_movie_without_auth(self, super_admin, common_user, new_movie_data):
        create_movie = super_admin.api.movie_api.create_movie(new_movie_data, expected_status=201)
        movie_id = create_movie.json()['id']

        response = common_user.api.movie_api.delete_movie(movie_id, expected_status=403)

    def test_patch_movie_with_invalid_data(self, super_admin, invalid_movie_data, movie_id):
        response = super_admin.api.movie_api.patch_movie(movie_id, invalid_movie_data, expected_status=400)
