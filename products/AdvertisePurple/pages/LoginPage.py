class LoginPage:
    def __init__(self, page):
        self.page = page
        # Locators
        self._username_txt = self.page.locator("//input[@name='email']")
        self._password_txt = self.page.locator("//input[@name='password']")
        self._sign_in_btn = self.page.locator("//span[@class='mat-button-wrapper' and text()='Sign In']")

    def enter_username(self, u_name):
        self._username_txt.fill(u_name)

    def enter_password(self, u_password):
        self._password_txt.fill(u_password)

    def click_sign_in(self):
        self._sign_in_btn.click()
