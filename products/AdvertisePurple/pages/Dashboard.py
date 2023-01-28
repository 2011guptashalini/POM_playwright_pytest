from playwright.sync_api import expect


class DashboardPage:
    def __init__(self, page):
        self.page = page
        # Locators
        self._dashboard_text = self.page.locator("//span[text()='My Clients']")

    @property
    def dashboard_page(self):
        return self._dashboard_text
