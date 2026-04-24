import pytest

from framework.utils.helpers import assert_booking_data_matches

@pytest.mark.api
@pytest.mark.booking
@pytest.mark.get
@pytest.mark.smoke
def test_successfully_get_booking(created_booking, booking_service, validate_booking):
    new_booking = created_booking["response_data"]

    # MAIN TESTS

    response = booking_service.get_booking(new_booking["id"])
    assert response.status_code == 200

    response_data = response.json()

    validate_booking(response_data)

    assert_booking_data_matches(response_data, created_booking["request_data"])