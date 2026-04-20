from framework.services.booking_service import BookingService
from framework.utils.data_generator import generate_booking_data

import pytest

from framework.utils.helpers import assert_booking_data_matches

@pytest.mark.post
@pytest.mark.booking
@pytest.mark.api
@pytest.mark.smoke
def test_post_booking(created_booking, booking_service, validate_booking):
    new_booking = created_booking["response_data"]

    validate_booking(new_booking)

    assert_booking_data_matches(new_booking, created_booking["request_data"])

    # id exists
    assert "id" in new_booking

    # verify we can retrieve the booking and it matches the created data
    get_response = booking_service.get_booking(new_booking["id"])
    assert get_response.status_code == 200
    assert_booking_data_matches(get_response.json(), new_booking)

@pytest.mark.post
@pytest.mark.booking
@pytest.mark.api
@pytest.mark.parametrize("field", ["first_name", "total_price", "check_in"])
def test_missing_field(booking_service, booking_data, field):
    del booking_data[field]

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422

@pytest.mark.post
@pytest.mark.booking
@pytest.mark.api
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

@pytest.mark.post
@pytest.mark.booking
@pytest.mark.api
@pytest.mark.parametrize("field, value", 
                         [
                             ("first_name", "a"*1000),
                             ("last_name", "a"*1000),
                             ("total_price", 1_000_001)
                         ],
                         ids=["first_name", "last_name", "total_price"])
def test_large_input(booking_service, booking_data, field, value):
    booking_data[field] = value

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422

@pytest.mark.post
@pytest.mark.booking
@pytest.mark.api
@pytest.mark.parametrize("field, value", 
                         [
                             ("first_name", ""),
                             ("last_name", ""),
                             ("total_price", "")
                         ],
                         ids=["first_name", "last_name", "total_price"])
def test_empty_field(booking_service, booking_data, field, value):
    booking_data[field] = value

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422

@pytest.mark.post
@pytest.mark.booking
@pytest.mark.api
@pytest.mark.parametrize("field, value", 
                         [
                             ("first_name", "<script>"),
                             ("last_name", "SELECT *")
                         ],
                         ids=["first_name", "last_name"])
def test_special_chars(booking_service, booking_data, field, value):
    booking_data[field] = value

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422