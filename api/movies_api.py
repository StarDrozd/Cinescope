from custom_requester.custom_requester import CustomRequester
from constants.constants import MOVIES_ENDPOINT, GENRES_ENDPOINT

class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session, base_url='https://api.dev-cinescope.coconutqa.ru')
        self.session = session

    def get_movies(self, expected_status=200, params=None):
        return self.send_request(
            method='GET',
            endpoint=MOVIES_ENDPOINT,
            expected_status=expected_status,
            params=params
        )
    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method='GET',
            endpoint=MOVIES_ENDPOINT + f'/{movie_id}',
            expected_status=expected_status
        )
    def create_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method='POST',
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )
    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method='DELETE',
            endpoint=MOVIES_ENDPOINT+f'/{movie_id}',
            expected_status=expected_status
        )
    def patch_movie(self, movie_id, updated_movie_data, expected_status=200):
        return self.send_request(
            method='PATCH',
            endpoint=MOVIES_ENDPOINT + f'/{movie_id}',
            data=updated_movie_data,
            expected_status=expected_status
        )
    def get_genres(self, expected_status=200):
        return self.send_request(
            method='GET',
            endpoint=GENRES_ENDPOINT,
            expected_status=expected_status
        )


