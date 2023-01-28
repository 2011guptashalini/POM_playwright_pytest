from playwright.sync_api import expect


class DashboardPage:
    def __init__(self, page):
        self.page = page
        # Locators

    def dashboard_displayed(self):
        expect(self.page).to_have_title("Advertise Purple Business Intelligence")
