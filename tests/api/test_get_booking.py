import pytest
from jsonschema import validate, ValidationError

@pytest.mark.get_booking
@pytest.mark.smoke
def test_get_booking_status(booking_service, bookings):
    response = booking_service.get_booking(bookings[0]["id"])
    assert response.status_code == 200

@pytest.mark.get_booking
def test_get_booking_structure(booking_service, bookings, validate_booking):
    response = booking_service.get_booking(bookings[0]["id"])
    booking = response.json()

    validate_booking(booking)

    assert "first_name" in booking
    assert "check_in" in booking

# validate direct get for newly created booking
@pytest.mark.get_booking
def test_get_new_booking_by_id(booking_service, booking_data, validate_booking):
    new_booking_response = booking_service.create_booking(booking_data)
    new_booking = new_booking_response.json()

    validate_booking(new_booking)

    booking_response = booking_service.get_booking(new_booking["id"])
    booking = booking_response.json()

    validate_booking(booking)

    assert booking["id"] == new_booking["id"]