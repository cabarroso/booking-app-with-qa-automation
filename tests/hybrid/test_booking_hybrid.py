import pytest

# Idea: to create a booking via API and verify it appears in the UI, then cleanup
@pytest.mark.hybrid
@pytest.mark.booking
@pytest.mark.create
def test_create_booking_via_api(booking_service, booking_data, bookings_page, validate_booking):

    # Create booking via API
    response = booking_service.create_booking(booking_data)
    api_response_new_booking = response.json()

    # Validate response against schema
    validate_booking(api_response_new_booking)

    # Open UI
    bookings_page.reload()

    # Verify new booking appears
    bookings_page_new_booking = bookings_page.get_booking_data_by_id(api_response_new_booking["id"])
    assert bookings_page_new_booking is not None
    assert bookings_page_new_booking["first_name"] == api_response_new_booking["first_name"]
    assert bookings_page_new_booking["last_name"] == api_response_new_booking["last_name"]
    assert bookings_page_new_booking["total_price"] == api_response_new_booking["total_price"]
    assert bookings_page_new_booking["deposit_paid"] == api_response_new_booking["deposit_paid"]
    assert bookings_page_new_booking["check_in"] == api_response_new_booking["check_in"]
    assert bookings_page_new_booking["check_out"] == api_response_new_booking["check_out"]
    assert bookings_page_new_booking["additional_needs"] == api_response_new_booking["additional_needs"]


    # cleanup
    booking_service.delete_booking(api_response_new_booking["id"])

@pytest.mark.hybrid
@pytest.mark.booking
@pytest.mark.delete
def test_delete_booking_via_api(booking_service, bookings_page):
    # Open UI and get last booking
    last_booking_id = bookings_page.get_last_booking_id()

    # Delete via API
    booking_service.delete_booking(last_booking_id)

    bookings_page.reload()

    # Verify
    assert bookings_page.get_last_booking_id() != last_booking_id
    