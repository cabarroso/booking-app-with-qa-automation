import pytest

from playwright.sync_api import expect

@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.bookings
def test_bookings_loaded(bookings_page):
    expect(bookings_page.heading_locator).to_be_visible()

@pytest.mark.ui
@pytest.mark.bookings
def test_delete_booking(bookings_page):
    deleted_id = bookings_page.get_last_booking_id()

    bookings_page.delete_last_booking()
    bookings_page.page.wait_for_load_state("networkidle")

    assert bookings_page.get_last_booking_id() != deleted_id