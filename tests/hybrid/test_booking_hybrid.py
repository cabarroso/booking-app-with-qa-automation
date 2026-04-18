import pytest
from playwright.sync_api import expect

from framework.utils.helpers import assert_booking_data_matches

# Idea: to create a booking via API and verify it appears in the UI, then cleanup
@pytest.mark.hybrid
@pytest.mark.booking
@pytest.mark.create
def test_create_booking_via_api(created_booking, booking_service, bookings_page, validate_booking):
    new_booking = created_booking["response_data"]

    # Validate response against schema
    validate_booking(new_booking)

    # Verify request and response data match for create booking API call
    assert_booking_data_matches(created_booking["request_data"], new_booking)

    # Verify booking is retrievable via API
    get_response = booking_service.get_booking(new_booking["id"])
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert_booking_data_matches(new_booking, get_data)

    # Verify new booking apears on page
    bookings_page.wait_for_booking_row(new_booking["id"])

    # Get booking data from UI
    ui_new_booking_data = bookings_page.get_booking_data_by_id(new_booking["id"])
    assert ui_new_booking_data is not None

    # Verify data shown on UI matches API response
    assert_booking_data_matches(new_booking, ui_new_booking_data)

# Idea: to create a booking via API, verify it appears in the UI, then delete via API and verify it no longer appears in the UI
@pytest.mark.hybrid
@pytest.mark.booking
@pytest.mark.delete
def test_delete_booking_via_api(created_booking, booking_service, bookings_page, validate_booking):
    new_booking = created_booking["response_data"]

    # Validate response against schema
    validate_booking(new_booking)

    # Verify request and response data match for create booking API call
    assert_booking_data_matches(created_booking["request_data"], new_booking)

    # Verify booking is retrievable via API
    get_response = booking_service.get_booking(new_booking["id"])
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert_booking_data_matches(new_booking, get_data)

    # MAIN TEST STEPS START HERE - DELETE AND VERIFY DISAPPEARANCE
    new_booking_id = new_booking["id"]

    # Verify new booking appears on page
    bookings_page.wait_for_booking_row(new_booking_id)

    # Delete via API
    delete_response = booking_service.delete_booking(new_booking_id)
    assert delete_response.status_code == 204

    # Verify booking is deleted via API
    get_response = booking_service.get_booking(new_booking_id)
    assert get_response.status_code == 404

    # Update page
    bookings_page.reload()

    # Verify booking row disappears from UI
    bookings_page.wait_for_booking_row_absence(new_booking_id)

    # Verify deleted booking is completely gone (not just hidden)
    assert not bookings_page.booking_row_is_present(new_booking_id)


