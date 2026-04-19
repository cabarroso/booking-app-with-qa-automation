import pytest

from framework.utils.helpers import assert_booking_data_matches

@pytest.mark.delete
@pytest.mark.api
def test_delete_booking_removes_booking(booking_service, created_booking, validate_booking):
    # SETUP - create a booking to delete
    new_booking = created_booking["response_data"]

    validate_booking(new_booking)

    assert_booking_data_matches(created_booking["request_data"], new_booking)

    # MAIN TESTS - delete the booking and verify it no longer exists

    new_booking_id = new_booking["id"]

    get_response = booking_service.get_booking(new_booking_id)
    assert get_response.status_code == 200

    delete_response = booking_service.delete_booking(new_booking_id)
    assert delete_response.status_code == 204

    get_response = booking_service.get_booking(new_booking_id)
    assert get_response.status_code == 404


@pytest.mark.delete
@pytest.mark.api
def test_delete_booking_invalid_id_returns_404(booking_service):
    get_response = booking_service.get_booking(0)
    assert get_response.status_code == 404

    delete_response = booking_service.delete_booking(0)
    assert delete_response.status_code == 404

    assert delete_response.json() == {"detail": "Booking not found"}