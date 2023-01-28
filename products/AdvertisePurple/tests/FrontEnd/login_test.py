from playwright.sync_api import Page, expect
from products.AdvertisePurple.pages.LoginPage import LoginPage
from products.AdvertisePurple.utils import utils as util
from products.AdvertisePurple.pages.LoginPage import LoginPage
from products.AdvertisePurple.pages.Dashboard import DashboardPage


class TestLogin:
    def test_valid_credentials(self, set_up_tear_down) -> None:
        page = set_up_tear_down
        login = LoginPage(page)
        login.enter_username(util.USERNAME)
        login.enter_password(util.PASSWORD)
        login.click_sign_in()
        dashboard = DashboardPage(page)
        if dashboard.dashboard_displayed() is True:
            print("Dashboard is displayed")
        else:
            print("Dashboard is not displayed")

