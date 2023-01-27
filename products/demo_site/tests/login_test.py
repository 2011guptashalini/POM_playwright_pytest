from playwright.sync_api import Page, expect
from products.demo_site.pages.LoginPage import LoginPage
from products.demo_site.tests import conftest


class TestLogin:
    def test_no_credentials(self, set_up_tear_down) -> None:
        page = set_up_tear_down
        try:
            login = LoginPage(page)
            login.enter_username(" ")
            login.enter_password(" ")
            login.click_sign_in()
        except AssertionError as error:
            raise error
            print(error)
