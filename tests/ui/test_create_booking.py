import pytest
import allure

from playwright.sync_api import expect

from framework.utils.helpers import assert_booking_data_matches
from pages.bookings_page import BookingsPage

@allure.title("UI Create Booking Page - Successfully Loaded")
@allure.description("Verify that the create booking page loads when accessed by user.")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.post
@pytest.mark.booking
def test_create_booking_successfully_loaded(create_booking_page):
    expect(create_booking_page.heading_locator).to_be_visible()


@allure.title("UI Create Booking Page - Successfully Create Booking")
@allure.description("Use the form on the page to successfully create a booking after user submits the form.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
@pytest.mark.post
@pytest.mark.smoke
@pytest.mark.booking
def test_create_booking(create_booking_page, booking_service, booking_data, validate_booking):
    # Catch post response info from POST
    with create_booking_page.page.expect_response("**/bookings") as response_info:
        create_booking_page.create_booking(booking_data)

    response = response_info.value
    assert response.status == 201

    new_booking = response.json()

    print(f"[SETUP] Created booking ID={new_booking['id']}")

    validate_booking(new_booking)

    assert_booking_data_matches(new_booking, booking_data)

    # wait for /bookings redirect
    create_booking_page.page.wait_for_load_state("networkidle")

    # confirm redirected away from create booking page
    expect(create_booking_page.heading_locator).not_to_be_visible()

    # verify new booking is present and visible in UI with correct data
    bookings_page = BookingsPage(create_booking_page.page)
    
    # confirm redirect to /bookings
    expect(bookings_page.heading_locator).to_be_visible()

    new_booking_id = new_booking["id"]

    # verify new booking is present and visible in UI...
    assert bookings_page.booking_row_is_present(new_booking_id)
    expect(bookings_page.get_booking_row_by_id(new_booking_id)).to_be_visible()

    # ...with correct data
    new_booking_ui_data = bookings_page.get_booking_data_by_id(new_booking_id)
    assert_booking_data_matches(new_booking_ui_data, new_booking)

    # CLEANUP - delete the created booking

    cleanup_response = booking_service.delete_booking(new_booking["id"])
    if cleanup_response.status_code not in [204, 404]:
        pytest.fail(f"Cleanup failed for booking ID={new_booking['id']} with status code {cleanup_response.status_code}")
    
    # verify booking is deleted and not present or visible in UI
    bookings_page.wait_for_booking_row_absence(new_booking_id)
    assert not bookings_page.booking_row_is_present(new_booking_id)
    expect(bookings_page.get_booking_row_by_id(new_booking_id)).not_to_be_visible()
    
    # log cleanup for CI visibility
    print(f"[TEARDOWN] Deleted booking ID={new_booking['id']}")



    
# @pytest.mark.ui
# @pytest.mark.create_booking
# def test_create_booking_invalid_input(create_booking_page, booking_data):
#     pass


