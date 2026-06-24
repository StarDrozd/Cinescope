from models.page_models.base_page import BasePage
from constants.constants import MOVIES_ENDPOINT
from playwright.sync_api import Page
import re

class CinescopeMoviePage(BasePage):
    def __init__(self, page: Page, id):
        super().__init__(page)
        self.url = f"{self.home_url}{MOVIES_ENDPOINT}/{id}"

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

    def assert_review_was_posted(self, review_text: str):
       self.page.get_by_text(review_text).is_visible()

    def assert_review_rating_correct(self, review_text: str, rating):
        self.page.locator("div").filter(has_text=re.compile(fr"^{review_text}\?Рейтинг: {rating}/5$")).locator("span").is_visible()

