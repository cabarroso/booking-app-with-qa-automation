import pytest

from playwright.sync_api import expect

@pytest.mark.ui
@pytest.mark.login
@pytest.mark.smoke
def test_login_page_loaded(login_page):
    expect(login_page.heading_locator).to_be_visible()

@pytest.mark.ui
@pytest.mark.login
def test_login(login_page):
    login_page.login("admin", "password123")
    expect(login_page.heading_locator).not_to_be_visible()
    assert not login_page.at_login_page
    expect(login_page.error_message_locator).not_to_be_visible()

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

