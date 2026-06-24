from models.page_models.base_page import BasePage
from playwright.sync_api import Page

class CinescopeMoviePage(BasePage):
    def __init__(self, page: Page, id):
        super().__init__(page)
        self.url = f"{self.home_url}movies/{id}"

        self.review_input = "textarea[data-qa-id='movie_review_input']"

        self.rating_button = "button[role='combobox']:has(span[data-qa-id='movie_rating_select'])"
        self.review_botton = "button[data-qa-id='movie_review_submit_button']"

    def open(self):
        self.open_url(self.url)

    def write_review(self, text_of_review: str):
        self.enter_text_to_element(self.review_input, text_of_review)

    def choose_rating(self, rating):
        self.click_element(self.rating_button)

        option = self.page.locator(f"div[role='option']:has-text('{rating}')")
        option.click()

    def post_review(self):
        self.click_element(self.review_botton)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Отзыв успешно создан")
