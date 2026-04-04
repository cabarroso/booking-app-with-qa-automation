from framework.services.booking_service import BookingService
from framework.utils.data_generator import generate_booking_data

import pytest

@pytest.mark.post_booking
def test_post_booking(booking_service, booking_data):
    response = booking_service.create_booking(booking_data)

    # status code
    assert response.status_code == 201

    response_data = response.json()

    # id exists
    assert "id" in response_data

    # all other fields are the same
    assert response_data["first_name"] == booking_data["first_name"]
    assert response_data["last_name"] == booking_data["last_name"]
    assert response_data["total_price"] == booking_data["total_price"]
    assert response_data["deposit_paid"] == booking_data["deposit_paid"]
    assert response_data["check_in"] == booking_data["check_in"]
    assert response_data["check_out"] == booking_data["check_out"]
    assert response_data["additional_needs"] == booking_data["additional_needs"]

@pytest.mark.post_booking
@pytest.mark.parametrize("field", ["first_name", "total_price", "check_in"])
def test_missing_field(booking_service, booking_data, field):
    del booking_data[field]

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422

@pytest.mark.post_booking
@pytest.mark.parametrize("field, value", 
                        [("first_name", 1337), 
                         ("total_price", "fifty"), 
                         ("check_in", 3.14),
                         ("deposit_paid", "notabool")],
                        ids=["first_name", "total_price", "check_in", "deposit_paid"])
def test_invalid_value_type(booking_service, booking_data, field, value):
    booking_data[field] = value

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422
