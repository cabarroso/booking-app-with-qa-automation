from typing import Generator

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from pages.bookings_page import BookingsPage
from pages.create_booking_page import CreateBookingPage
from pages.login_page import LoginPage

@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    yield page

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login_page = LoginPage(page)
    login_page.open()
    return login_page

@pytest.fixture
def valid_login(login_page: LoginPage) -> Page:
    login_page.login("admin", "password123")
    login_page.page.wait_for_load_state("networkidle") # wait for /bookings redirect
    return login_page.page

@pytest.fixture
def create_booking_page(valid_login: Page) -> CreateBookingPage:
    create_booking_page = CreateBookingPage(valid_login)
    create_booking_page.open()
    return create_booking_page

@pytest.fixture
def bookings_page(valid_login: Page) -> BookingsPage:
    bookings_page = BookingsPage(valid_login)
    bookings_page.open()
    return bookings_page

