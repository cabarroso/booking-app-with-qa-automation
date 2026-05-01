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
    with allure.step("Expect login page heading to be visible"):
        expect(login_page.heading_locator).to_be_visible()

@allure.title("UI Login Page - Successful Login")
@allure.description("User is able to successfully login with valid credentials.")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.ui
@pytest.mark.login
def test_login(login_page):
    with allure.step("Login via UI with valid credentials"):
        login_page.login("admin", "password123")
    
    with allure.step("Verify page redirects away from login page"):
        expect(login_page.heading_locator).not_to_be_visible()
        assert not login_page.at_login_page

    with allure.step("Expect error message not to be visible"):
        expect(login_page.error_message_locator).not_to_be_visible()

@allure.title("UI Login Page - Failed Login with Empty Input Value")
@allure.description("User fails to login with empty username or password values")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
@pytest.mark.login
@pytest.mark.parametrize("username, password", 
                         [
                             ("", "password123"),
                             ("admin", ""),
                         ],
                         ids=["username", "password"]
                        )
def test_login_empty_input(login_page, username, password):
    with allure.step("Attempt login with an empty field value"):
        login_page.login(username, password)

    with allure.step("Verify that we are still at the login page"):
        expect(login_page.heading_locator).to_be_visible()
        assert login_page.at_login_page

    with allure.step("Expect error message to be visible"):
        expect(login_page.error_message_locator).to_be_visible()

