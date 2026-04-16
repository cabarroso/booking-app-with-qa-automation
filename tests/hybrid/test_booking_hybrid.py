import pytest
from playwright.sync_api import expect

# Idea: to create a booking via API and verify it appears in the UI, then cleanup
@pytest.mark.hybrid
@pytest.mark.booking
@pytest.mark.create
def test_create_booking_via_api(booking_service, booking_data, bookings_page, validate_booking):

    # Create booking via API
    response = booking_service.create_booking(booking_data)

    # Verify API response and data matches what we sent
    assert response.status_code == 201
    api_response_new_booking = response.json()
    assert_booking_data_matches(booking_data, api_response_new_booking)

    # Validate response against schema
    validate_booking(api_response_new_booking)

    #reload UI to ensure it reflects latest data
    bookings_page.reload()

    # Log creation for CI visibility
    print(f"[STEP] Created booking ID={api_response_new_booking['id']}")

    # Verify new booking appears on page and data matches API response using UI
    try:
        bookings_page.wait_for_booking(api_response_new_booking["id"])
        bookings_page_new_booking = bookings_page.get_booking_data_by_id(api_response_new_booking["id"])
        assert bookings_page_new_booking is not None
        assert_booking_data_matches(api_response_new_booking, bookings_page_new_booking)
        
    finally:
        # cleanup
        cleanup_response = booking_service.delete_booking(api_response_new_booking["id"])
        if cleanup_response.status_code not in [204, 404]:
            raise Exception("Cleanup failed")
        # log cleanup for CI visibility
        print(f"[STEP] Cleaned up booking ID={api_response_new_booking['id']}")

# Idea: to create a booking via API, verify it appears in the UI, then delete via API and verify it no longer appears in the UI
@pytest.mark.hybrid
@pytest.mark.booking
@pytest.mark.delete
def test_delete_booking_via_api(booking_service, booking_data, bookings_page, validate_booking):
    # Create booking via API
    response = booking_service.create_booking(booking_data)

    # Verify API response and data matches what we sent
    assert response.status_code == 201
    new_booking = response.json()
    assert_booking_data_matches(booking_data, new_booking)

    # Validate response against schema
    validate_booking(new_booking)
    new_booking_id = new_booking["id"]

    # Open UI
    bookings_page.reload()

    # log creation for CI visibility
    print(f"[STEP] Created booking ID={new_booking_id}")

    try:
        # Verify new booking appears on page
        bookings_page.wait_for_booking(new_booking_id)

        # Delete via API
        delete_response = booking_service.delete_booking(new_booking_id)
        assert delete_response.status_code == 204

        # Verify booking is deleted via API
        get_response = booking_service.get_booking(new_booking_id)
        assert get_response.status_code == 404

        bookings_page.reload()

        # Verify deleted booking no longer appears on page (not just hidden)
        assert not bookings_page.booking_row_is_present(new_booking_id)
    finally:
        try:
            # cleanup in case fail before delete
            booking_service.delete_booking(new_booking_id)
            # log cleanup for CI visibility
            print(f"[STEP] Cleaned up booking ID={new_booking_id}")
        except Exception:
            pass

# helper function to compare and assert booking data matches
def assert_booking_data_matches(booking_data1, booking_data2):
    assert booking_data1["first_name"] == booking_data2["first_name"]
    assert booking_data1["last_name"] == booking_data2["last_name"]
    assert booking_data1["total_price"] == booking_data2["total_price"]
    assert booking_data1["deposit_paid"] == booking_data2["deposit_paid"]
    assert booking_data1["check_in"] == booking_data2["check_in"]
    assert booking_data1["check_out"] == booking_data2["check_out"]
    assert booking_data1["additional_needs"] == booking_data2["additional_needs"]
