from http.client import responses

import pytest
import requests

from conftest import admin_auth, movie_id
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT, MOVIE_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager
class TestMoviesAPI:
    def test_get_movies(self, api_manager: ApiManager):
        response = api_manager.movie_api.get_movies()
        response_data = response.json()

        assert response_data != {}

    def test_get_movies_with_params(self, api_manager: ApiManager, get_params):
        response = api_manager.movie_api.get_movies(params=get_params)
        response_data = response.json()

        assert response_data != {}
        assert len(response_data['movies'])==get_params['pageSize']

    def test_get_movie(self, api_manager: ApiManager, movie_id):
        response = api_manager.movie_api.get_movie(movie_id)
        response_data = response.json()

        assert  response_data['id'] == movie_id

    def test_create_movie(self, admin_auth, new_movie_data):
        response = admin_auth.movie_api.create_movie(new_movie_data)
        response_data = response.json()

        assert response_data['name'] == new_movie_data['name']

    def test_delete_movie(self, api_manager:ApiManager, admin_auth, movie_id):
        response = admin_auth.movie_api.delete_movie(movie_id)

        checking = api_manager.movie_api.get_movie(movie_id, expected_status=404)
        assert checking.status_code == 404, 'Фильм не удален'

    def test_patch_movie(self, admin_auth, movie_id, new_movie_data, updated_movie_data):
        response = admin_auth.movie_api.patch_movie(movie_id, updated_movie_data)

        assert response.json()['name'] != new_movie_data['name']

class TestNegativeMoviesAPI:
    def test_get_nonexistent_movie(self, api_manager: ApiManager):
        movie_id =  88*14 * 37* 51  #делаем несуществующий айди
        response = api_manager.movie_api.get_movie(movie_id, expected_status=404)

    def test_create_conflict_movie(self, admin_auth, new_movie_data):
        new_movie_data['name'] = 'Название фильма'
        response = admin_auth.movie_api.create_movie(new_movie_data, expected_status=409)

    def test_create_movie_with_invalid_data(self, admin_auth, invalid_movie_data):
        response = admin_auth.movie_api.create_movie(invalid_movie_data, expected_status=400)

    def test_create_movie_without_auth(self, api_manager: ApiManager, new_movie_data):
        response = api_manager.movie_api.create_movie(new_movie_data, expected_status=401)

    def test_delete_movie_without_auth(self, api_manager: ApiManager):
        movie_id = 463
        response = api_manager.movie_api.delete_movie(movie_id, expected_status=401)

    def test_delete_movie_nonexistent_movie(self, admin_auth):
        movie_id = '31f013131'
        response = admin_auth.movie_api.delete_movie(movie_id, expected_status=404)

    def test_patch_movie_with_invalid_data(self, admin_auth, invalid_movie_data, movie_id):
        response = admin_auth.movie_api.patch_movie(movie_id, invalid_movie_data, expected_status=400)
