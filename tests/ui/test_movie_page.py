import allure
import pytest               
from faker import Faker
from playwright.sync_api import sync_playwright
from models.page_models.login_page import CinescopeLoginPage
from models.page_models.movie_page import CinescopeMoviePage
faker = Faker()

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Movie/id")
@pytest.mark.ui
class TestMoviePage:

    @allure.title("Успешное создание отзыва пользователем")
    def test_post_review(self, movie_id, registered_user, review_text = 'the best movie ever. 10/10', rating = faker.random_int(1,5)):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            login_page = CinescopeLoginPage(page)
            login_page.open()
            login_page.login(registered_user['email'], registered_user['password'])
            login_page.assert_error_was_pop_up()
            login_page.reload_page()

            movie_page = CinescopeMoviePage(page, movie_id)
            movie_page.open()

            movie_page.write_review(review_text)
            movie_page.choose_rating(rating)
            movie_page.post_review()

            movie_page.assert_allert_was_pop_up()
            movie_page.assert_review_was_posted(review_text)
            movie_page.assert_review_rating_correct(review_text, rating)