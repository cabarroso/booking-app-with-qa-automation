import pytest

from playwright.sync_api import expect

from pages.bookings_page import BookingsPage

@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.create_booking
def test_create_booking_loaded(create_booking_page):
    expect(create_booking_page.heading_locator).to_be_visible()

@pytest.mark.ui
@pytest.mark.create_booking
def test_create_booking(create_booking_page, booking_data):
    create_booking_page.create_booking(booking_data)

    # wait for /bookings redirect
    create_booking_page.page.wait_for_load_state("networkidle")

    # confirm redirected
    expect(create_booking_page.heading_locator).not_to_be_visible()

    # verify new booking in /bookings
    bookings_page = BookingsPage(create_booking_page.page)
    assert bookings_page.get_last_booking_first_name() == booking_data["first_name"]
    assert bookings_page.get_last_booking_last_name() == booking_data["last_name"]
    assert bookings_page.get_last_booking_total_price() == booking_data["total_price"]
    

# @pytest.mark.ui
# @pytest.mark.create_booking
# def test_create_booking_invalid_input(create_booking_page, booking_data):
#     booking_data["first_name"]


