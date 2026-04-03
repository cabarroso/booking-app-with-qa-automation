
from playwright.sync_api import Locator, Page

class LoginPage():

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("http://localhost:5173/login")

    @property
    def username_input_locator(self) -> Locator:
        return self.page.get_by_role("textbox", name="Username")
    
    @property
    def password_input_locator(self) -> Locator:
        pass

    @property
    def login_button_locator(self):
        return self.page.get_by_role("button", name="Login")
    
    def fill_username(self, username):
        self.username_input_locator.fill(username)

    def fill_password(self, password):
        self.password_input_locator.fill(password)

    def submit(self):
        self.login_button_locator.click()

    def login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.submit()
