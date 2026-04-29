import pytest
import allure

from framework.utils.helpers import assert_booking_data_matches

@allure.title("Get Booking - Valid ID")
@allure.description("Verify that the API successfully retrieves a booking with a valid ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.get
@pytest.mark.smoke
def test_successfully_get_booking(created_booking, booking_service, validate_booking):
    
    with allure.step("[SETUP] Create a new booking"):
        new_booking = created_booking["response_data"]

    # MAIN TESTS
    with allure.step("Make a GET request with ID from the new booking"):
        response = booking_service.get_booking(new_booking["id"])

    with allure.step("Verify response contains status code of 200"):
        assert response.status_code == 200

    response_data = response.json()

    with allure.step("Validate response payload against the Booking schema"):
        validate_booking(response_data)

    with allure.step("Verify response payload contains identical booking data to the initial request data that created the new booking"):
        assert_booking_data_matches(response_data, created_booking["request_data"])