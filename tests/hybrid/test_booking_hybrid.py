import pytest
import allure

from playwright.sync_api import expect

from framework.utils.helpers import assert_booking_data_matches

# Idea: to create a booking via API and verify it appears in the UI, then cleanup
@allure.title("Hybrid Create Booking - Successfully Create Booking")
@allure.description("Creating a booking via API results in a booking row created on the Bookings Page.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.hybrid
@pytest.mark.booking
@pytest.mark.create
def test_create_booking_via_api(created_booking, booking_service, bookings_page, validate_booking):
    
    with allure.step("Create a new booking"):
        new_booking = created_booking["response_data"]

    with allure.step("Validate new booking against schema"):
        # Validate response against schema
        validate_booking(new_booking)

    with allure.step("Verify new booking data matches its request data"):
        # Verify request and response data match for create booking API call
        assert_booking_data_matches(created_booking["request_data"], new_booking)

    with allure.step("Verify new booking is accessible via API GET request to bookings/{id}"):
    # Verify booking is retrievable via API
        get_response = booking_service.get_booking(new_booking["id"])
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert_booking_data_matches(new_booking, get_data)

    with allure.step("Expect booking row for new booking to be visible in Bookings Page"):
        # Verify new booking apears on page
        bookings_page.wait_for_booking_row(new_booking["id"])

    with allure.step("Extract data from the new booking row in UI"):
        # Get booking data from UI
        ui_new_booking_data = bookings_page.get_booking_data_by_id(new_booking["id"])
        assert ui_new_booking_data is not None

    with allure.step("Verify data from UI matches the origin request data"):
        # Verify data shown on UI matches API response
        assert_booking_data_matches(created_booking["request_data"], ui_new_booking_data)

# Idea: to create a booking via API, verify it appears in the UI, then delete via API and verify it no longer appears in the UI
@allure.title("Hybrid Delete Booking - Successfully Delete Booking")
@allure.description("Deleting a booking via API deletes the corresponding row in the UI for Bookings Page.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.hybrid
@pytest.mark.booking
@pytest.mark.delete
def test_delete_booking_via_api(created_booking, booking_service, bookings_page, validate_booking):
    with allure.step("Create a new booking"):
        new_booking = created_booking["response_data"]

    with allure.step("Validate new booking against schema"):
        # Validate response against schema
        validate_booking(new_booking)

    with allure.step("Verify new booking data matches request data"):
        # Verify request and response data match for create booking API call
        assert_booking_data_matches(created_booking["request_data"], new_booking)

    with allure.step("Verify new booking is accessible via API GET request to /bookings/{id}"):
    # Verify booking is retrievable via API
        get_response = booking_service.get_booking(new_booking["id"])
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert_booking_data_matches(new_booking, get_data)

    # MAIN TEST STEPS START HERE - DELETE AND VERIFY DISAPPEARANCE
    new_booking_id = new_booking["id"]

    with allure.step("Expect new booking row to appear in Bookings Page"):
        # Verify new booking appears on page
        bookings_page.wait_for_booking_row(new_booking_id)

    with allure.step("Delete new booking via API"):
        # Delete via API
        delete_response = booking_service.delete_booking(new_booking_id)

    with allure.step("Verify status code 204"):
        assert delete_response.status_code == 204

    with allure.step("Attempt to delete the same booking again"):
        # Verify booking is deleted via API
        get_response = booking_service.get_booking(new_booking_id)

    with allure.step("Verify status code 404"):
        assert get_response.status_code == 404

    # Update page
    bookings_page.reload()

    with allure.step("Expect booking row to not be visible or present in Bookings Page"):
        # Verify booking row disappears from UI
        bookings_page.wait_for_booking_row_absence(new_booking_id)
        # Verify deleted booking is completely gone (not just hidden)
        assert not bookings_page.booking_row_is_present(new_booking_id)


