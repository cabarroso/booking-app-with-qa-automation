import pytest

from playwright.sync_api import expect

@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.create_booking
def test_create_booking_loaded(create_booking_page):
    expect(create_booking_page.heading_locator).to_be_visible()

@pytest.mark.ui
@pytest.mark.create_booking
def test_create_booking(create_booking_page, booking_data):
    create_booking_page.create_booking(booking_data)
    create_booking_page.page.wait_for_load_state("networkidle")

    expect(create_booking_page.heading_locator).not_to_be_visible()

@pytest.mark.ui
@pytest.mark.create_booking
def test_create_booking_invalid_input(create_booking_page, booking_data):
    pass


