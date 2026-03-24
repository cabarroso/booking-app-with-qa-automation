from framework.services.booking_service import BookingService
from framework.utils.data_generator import generate_booking_data

import pytest

def test_create_booking():
    test_booking_data = generate_booking_data()
    response = BookingService().create_booking(test_booking_data)

    # status code
    assert response.status_code == 201

    response_data = response.json()

    # id exists
    assert "id" in response_data

    # all other fields are the same
    assert response_data["first_name"] == test_booking_data["first_name"]
    assert response_data["last_name"] == test_booking_data["last_name"]
    assert response_data["total_price"] == test_booking_data["total_price"]
    assert response_data["deposit_paid"] == test_booking_data["deposit_paid"]
    assert response_data["check_in"] == test_booking_data["check_in"]
    assert response_data["check_out"] == test_booking_data["check_out"]
    assert response_data["additional_needs"] == test_booking_data["additional_needs"]

@pytest.mark.parametrize("field", 
                         ["first_name", "total_price", "check_in"])
def test_missing_field(field):
    booking_data = generate_booking_data()
    del booking_data[field]

    response = BookingService().create_booking(booking_data)

    assert response.status_code == 422
