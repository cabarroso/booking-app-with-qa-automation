import pytest

from framework.utils.helpers import assert_booking_data_matches

@pytest.mark.smoke
@pytest.mark.delete
@pytest.mark.api
def test_delete_booking_status(booking_service, created_booking, validate_booking):
    # SETUP - create a booking to delete
    new_booking = created_booking["response_data"]

    validate_booking(new_booking)

    assert_booking_data_matches(created_booking["request_data"], new_booking)

    # MAIN TESTING - delete the booking and verify status code

    response = booking_service.delete_booking(new_booking["id"])

    assert response.status_code == 204

@pytest.mark.delete_booking
def test_delete_booking(booking_service, last_booking_id):
    response = booking_service.get_booking(last_booking_id)
    assert response.status_code == 200

    booking_service.delete_booking(last_booking_id)

    response = booking_service.get_booking(last_booking_id)
    assert response.status_code == 404


@pytest.mark.delete_booking
def test_delete_booking_id_doesnt_exist(booking_service, last_booking_id):
    response = booking_service.delete_booking(last_booking_id + 1)

    assert response.status_code == 404