import pytest

from framework.utils.helpers import assert_booking_data_matches

@pytest.mark.get
@pytest.mark.bookings
@pytest.mark.api
@pytest.mark.smoke
def test_get_bookings_not_empty(created_booking, booking_service, validate_booking):
    new_booking = created_booking["response_data"]

    validate_booking(new_booking)

    assert_booking_data_matches(new_booking, created_booking["request_data"])

    # MAIN TEST - verify new booking appears in list and details match
    get_bookings_response = booking_service.get_bookings()
    assert get_bookings_response.status_code == 200
    bookings = get_bookings_response.json()
    assert isinstance(bookings, list)

    get_booking_response = booking_service.get_booking(new_booking["id"])
    assert get_booking_response.status_code == 200

    get_booking_data = get_booking_response.json()

    validate_booking(get_booking_data)

    assert_booking_data_matches(get_booking_data, new_booking)

# make sure dicts in list have relevant fields
@pytest.mark.get_bookings
def test_get_bookings_structure(booking_service, bookings_response):
    # response = booking_service.get_bookings()
    bookings = bookings_response.json()
    
    assert "id" in bookings[0]
    assert "first_name" in bookings[0]
    assert "check_in" in bookings[0]

# validate route contains newly created bookings
@pytest.mark.get_bookings
def test_get_new_booking_in_bookings(booking_service, booking_data):
    new_booking_response = booking_service.create_booking(booking_data)
    bookings_response = booking_service.get_bookings()

    new_booking = new_booking_response.json()
    bookings = bookings_response.json()

    assert bookings[-1]["id"] == new_booking["id"]
    
    
