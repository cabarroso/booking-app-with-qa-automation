import pytest
import allure

from playwright.sync_api import expect

@allure.title("UI Login Page - Successfully Loaded")
@allure.description("Login page successfully loads when accessed by user.")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.ui
@pytest.mark.login
@pytest.mark.smoke
def test_login_page_loaded(login_page):
    expect(login_page.heading_locator).to_be_visible()

@allure.title("UI Login Page - Successful Login")
@allure.description("User is able to successfully login with valid credentials.")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.ui
@pytest.mark.login
def test_login(login_page):
    login_page.login("admin", "password123")
    expect(login_page.heading_locator).not_to_be_visible()
    assert not login_page.at_login_page
    expect(login_page.error_message_locator).not_to_be_visible()

@allure.title("UI Login Page - Failed Login with invalid Credentials")
@allure.description("User fails to login with invalid credentials.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
@pytest.mark.login
@pytest.mark.parametrize("username, password", 
                         [
                             ("", "password123"),
                             ("admin", ""),
                             ("", "")
                         ],
                         ids=["no username", "no password", "no username or password"]
                        )
def test_login_invalid_credentials(login_page, username, password):
    login_page.login(username, password)
    expect(login_page.heading_locator).to_be_visible()
    assert login_page.at_login_page
    expect(login_page.error_message_locator).to_be_visible()

