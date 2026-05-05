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

    with allure.step("[SETUP] Create booking"):
        # SETUP - create a booking to delete
        new_booking = created_booking["response_data"]

    # MAIN TESTS - delete the booking and verify it no longer exists
    new_booking_id = new_booking["id"]

    with allure.step("Verify GET request for the new booking is successful prior to deletion"):
        pre_delete_response = booking_service.get_booking(new_booking_id)
        assert pre_delete_response.status_code == 200

    with allure.step("DELETE the new booking"):
        delete_response = booking_service.delete_booking(new_booking_id)

    with allure.step("Verify DELETE response contains status of 204"):
        assert delete_response.status_code == 204

    with allure.step("Verify no payload is present in DELETE response"):
        assert not delete_response.content

    with allure.step("Verify GET request for the new booking fails after deletion"):
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
    # MAIN TEST
    with allure.step("Attempt to DELETE a booking with an invalid ID number"):
        delete_response = booking_service.delete_booking(booking_id)
        
    with allure.step("Verify DELETE response contains staus of 422"):
        assert delete_response.status_code == 422

    error = delete_response.json()
    
    with allure.step("Verify response payload detail contains 'type' of 'greater_than_equal"):
        assert error["detail"][0]["type"] == "greater_than_equal"

    with allure.step("Verify response payload detail contains 'loc' of 'booking_id'"):
        assert error["detail"][0]["loc"][-1] == "booking_id"