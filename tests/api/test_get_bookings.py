from typing import List

import pytest

from framework.services.booking_service import BookingService
from framework.utils.data_generator import generate_booking_data

@pytest.mark.get
def test_get_bookings(booking_service):
    response = booking_service.get_bookings()
    assert response.status_code == 200
    bookings = response.json()
    assert isinstance(bookings, List)
    assert isinstance(bookings[0]["first_name"], str)
    
