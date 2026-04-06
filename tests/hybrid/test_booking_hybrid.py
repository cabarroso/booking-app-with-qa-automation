import pytest

@pytest.mark.hybrid
@pytest.mark.booking
def test_create_booking_via_api(booking_service, booking_data, bookings_page):
    # Create booking via API
    response = booking_service.create_booking(booking_data)

    assert response.status_code == 201

    new_booking = response.json()

    # Open UI
    bookings_page.reload()

    # Verify booking appears
    assert bookings_page.get_last_booking_id() == new_booking["id"]
    assert bookings_page.get_last_booking_first_name() == new_booking["first_name"]
    assert bookings_page.get_last_booking_last_name() == new_booking["last_name"]

    # cleanup
    booking_service.delete_booking(new_booking["id"])

@pytest.mark.hybrid
@pytest.mark.booking
def test_delete_booking_via_api(booking_service, bookings_page):
    # Open UI and get last booking
    last_booking_id = bookings_page.get_last_booking_id()

    # Delete via API
    response = booking_service.delete_booking(last_booking_id)

    bookings_page.reload()

    # Verify
    assert bookings_page.get_last_booking_id() != last_booking_id
    