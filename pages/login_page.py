
from playwright.sync_api import Locator, Page

from config import UI_BASE_URL

class LoginPage():

    def __init__(self, page: Page):
        self.page = page
        self.base_url = f"{UI_BASE_URL}/login"
    
    @property
    def current_url(self) -> str:
        return self.page.url

    @property
    def heading_locator(self) -> Locator:
        return self.page.get_by_role("heading", name="Login")

    @property
    def username_input_locator(self) -> Locator:
        return self.page.get_by_role("textbox", name="Username")
    
    @property
    def password_input_locator(self) -> Locator:
        return self.page.locator("#password")

    @property
    def login_button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Login")
    
    @property
    def error_message_locator(self) -> Locator:
        return self.page.locator(".error-message")
    
    @property
    def at_login_page(self) -> bool:
        return self.current_url == self.base_url
    
    def open(self):
        self.page.goto(self.base_url)
    
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

    
