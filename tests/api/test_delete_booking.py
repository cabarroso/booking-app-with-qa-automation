import allure
import pytest

from framework.utils.helpers import assert_booking_data_matches

@allure.title("Delete Booking - Valid ID")
@allure.description("Verify that the API successfully deletes a booking with a valid ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.delete
def test_delete_booking_removes_booking(booking_service, created_booking):
    # SETUP - create a booking to delete
    new_booking = created_booking["response_data"]

    # MAIN TESTS - delete the booking and verify it no longer exists
    new_booking_id = new_booking["id"]

    pre_delete_response = booking_service.get_booking(new_booking_id)
    assert pre_delete_response.status_code == 200

    assert_booking_data_matches(new_booking, pre_delete_response.json())

    delete_response = booking_service.delete_booking(new_booking_id)
    assert delete_response.status_code == 204
    assert not delete_response.content

    post_delete_response = booking_service.get_booking(new_booking_id)
    assert post_delete_response.status_code == 404

@allure.title("Delete Booking - Invalid ID")
@allure.description("Verify that the API returns a 422 error when attempting to delete a booking with an invalid ID (e.g., zero or negative)")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.delete
@pytest.mark.parametrize("booking_id", [0, -1], ids=["zero_id", "negative_id"])
def test_delete_booking_invalid_id_returns_422(booking_service, booking_id):
    # MAIN TEST - attempt to delete a non-existent booking and verify 422 response

    delete_response = booking_service.delete_booking(booking_id)
    assert delete_response.status_code == 422

    error = delete_response.json()
    assert error["detail"][0]["type"] == "greater_than_equal"
    assert error["detail"][0]["loc"][-1] == "booking_id"