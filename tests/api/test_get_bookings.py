from typing import List

import pytest

# basic test to show there are no obvious errors (should pass even if db is empty)
@pytest.mark.get_bookings
@pytest.mark.smoke
def test_get_bookings_status_and_type(booking_service, bookings_response):
    assert bookings_response.status_code == 200
    bookings = bookings_response.json()
    assert isinstance(bookings, List)

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
    
    
