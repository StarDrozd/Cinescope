import time
from faker import Faker
from playwright.sync_api import sync_playwright
from models.page_object_models import CinecsopeMoviePage, CinescopLoginPage
faker = Faker()

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Movie/id")
@pytest.mark.ui
class TestMoviePage:
@allure.title("Успешное создание отзыва пользователем")
def test_post_review(movie_id, registered_user):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        login_page = CinescopLoginPage(page)
        login_page.open()
        login_page.login(registered_user['email'], registered_user['password'])
        time.sleep(3)
        login_page.reload_page()

        movie_page = CinecsopeMoviePage(page, movie_id)
        movie_page.open()

        movie_page.write_review('the best movie ever. 10/10')
        movie_page.choose_rating(faker.random_int(min=1, max=5))
        movie_page.post_review()
        time.sleep(3)

        movie_page.assert_allert_was_pop_up()
        time.sleep(2)