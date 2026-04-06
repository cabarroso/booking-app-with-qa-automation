import pytest

@pytest.mark.hybrid
@pytest.mark.booking
def test_create_booking_via_api(booking_service, booking_data, bookings_page):
    # Create booking via API
    response = booking_service.create_booking(booking_data)

    assert response.status_code == 201

    new_booking = response.json()

    # Open UI
    bookings_page.page.reload()

    # Verify booking appears
    assert bookings_page.get_last_booking_id() == new_booking["id"]
    