import pytest
import allure

from playwright.sync_api import expect

from framework.utils.helpers import assert_booking_data_matches

@allure.title("UI Bookings Page - Successfully Loaded")
@allure.description("Verify that bookings page successfully loads")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.bookings
def test_bookings_page_successfully_loaded(bookings_page):
    with allure.step("Expect page heading to be visible"):
        expect(bookings_page.heading_locator).to_be_visible()

@allure.title("UI Bookings Page - Delete a Booking")
@allure.description("Verify that clicking on the delete button will delete the corresponding booking from the page.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
@pytest.mark.bookings
@pytest.mark.delete
def test_delete_booking_from_bookings_page(bookings_page, created_booking, booking_service, validate_booking):
    with allure.step("Create a new booking"):
        new_booking = created_booking["response_data"]

    bookings_page.wait_for_booking_row(new_booking["id"])

    # MAIN TESTS

    # Before deleting, assert booking row is present and visible in UI
    with allure.step("Verify that the booking row is present and visible"):
        assert bookings_page.booking_row_is_present(new_booking["id"])
        expect(bookings_page.get_booking_row_by_id(new_booking["id"])).to_be_visible()
    
    with allure.step("Click 'delete' on the new booking row in the UI"):
        # Delete booking via UI
        bookings_page.delete_booking_by_id(new_booking["id"])
    
    bookings_page.page.wait_for_load_state("networkidle")

    with allure.step("Verify the new booking row is no longer present or visible"):
        # After deletion, assert booking row is no longer present and visible in UI
        assert not bookings_page.booking_row_is_present(new_booking["id"])
        expect(bookings_page.get_booking_row_by_id(new_booking["id"])).not_to_be_visible()