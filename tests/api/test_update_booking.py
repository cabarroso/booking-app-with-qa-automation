import pytest

from framework.utils.helpers import assert_booking_data_matches

@pytest.mark.put
@pytest.mark.api
@pytest.mark.booking
def test_update_booking(created_booking, booking_service, booking_data, validate_booking):
    new_booking = created_booking["response_data"]

    validate_booking(new_booking)

    assert_booking_data_matches(new_booking, created_booking["request_data"])

    # MAIN TESTS
    put_response = booking_service.update_booking(new_booking["id"], booking_data)
    assert put_response.status_code == 200
    updated_booking = put_response.json()

    validate_booking(updated_booking)

    assert updated_booking["id"] == new_booking["id"]
    assert_booking_data_matches(updated_booking, booking_data)

@pytest.mark.put
@pytest.mark.api
@pytest.mark.booking
def test_update_booking_id_doesnt_exist(booking_service, booking_data):
    response = booking_service.update_booking(0, booking_data)

    assert response.status_code >= 400

@pytest.mark.put
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.parametrize("field", ["first_name", "total_price", "check_in"])
def test_update_booking_missing_field(created_booking, booking_service, booking_data, validate_booking, field):
    new_booking = created_booking["response_data"]

    validate_booking(new_booking)

    assert_booking_data_matches(new_booking, created_booking["request_data"])

    # MAIN TESTS
    
    del booking_data[field]

    response = booking_service.update_booking(new_booking["id"], booking_data)

    assert response.status_code == 422

@pytest.mark.put
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.parametrize("field, value", 
                        [("first_name", 1337),
                         ("total_price", "fifty dollars"),
                         ("check_in", 3.14),
                         ("deposit_paid", "notabool")],
                        ids=["first_name", "total_price", "check_in", "deposit_paid"])
def test_update_booking_invalid_value_type(created_booking, booking_service, booking_data, validate_booking, field, value):
    new_booking = created_booking["response_data"]

    validate_booking(new_booking)

    assert_booking_data_matches(new_booking, created_booking["request_data"])

    # MAIN TESTS

    booking_data[field] = value

    response = booking_service.update_booking(new_booking["id"], booking_data)

    assert response.status_code == 422
