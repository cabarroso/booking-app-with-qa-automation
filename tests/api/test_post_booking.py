import pytest
import allure

from framework.utils.helpers import assert_booking_data_matches

@allure.title("API Post Booking - Successfully Created Booking")
@allure.description("Test that a booking can be created when all required fields are provided with valid data")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.post
@pytest.mark.smoke
def test_successfully_post_booking(created_booking, booking_service, validate_booking):
    request_data = created_booking["request_data"]
    new_booking = created_booking["response_data"]

    validate_booking(new_booking)

    assert_booking_data_matches(new_booking, request_data)

    # id exists
    assert "id" in new_booking

    # verify we can retrieve the booking and it matches the created data
    response = booking_service.get_booking(new_booking["id"])

    assert response.status_code == 200
    assert_booking_data_matches(response.json(), request_data)

@allure.title("API Post Booking - Missing Field")
@allure.description("Verify that the API returns a 422 error when required fields are missing from the booking creation request")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.post
@pytest.mark.parametrize("field", ["first_name", "total_price", "check_in"])
def test_missing_field_status_422(booking_service, booking_data, field):
    assert field in booking_data
    del booking_data[field]

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422

    fail_response_data = response.json()
    assert fail_response_data["detail"][0]["msg"] == "Field required"
    assert fail_response_data["detail"][0]["loc"][-1] == field

@allure.title("API Post Booking - Invalid Value Type for Field")
@allure.description("Verify that the API returns a 422 error when fields in the booking creation request have invalid data types")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.post
@pytest.mark.parametrize("field, value, detail_type", 
                        [("first_name", 1337, "string_type"), 
                         ("total_price", "fifty", "int_parsing"), 
                         ("check_in", 3.14, "date_from_datetime_inexact"),
                         ("deposit_paid", "notabool", "bool_parsing")],
                        ids=["first_name", "total_price", "check_in", "deposit_paid"])
def test_invalid_value_type_status_422(booking_service, booking_data, field, value, detail_type):
    booking_data[field] = value

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422

    fail_response_data = response.json()
    assert fail_response_data["detail"][0]["type"] == detail_type
    assert fail_response_data["detail"][0]["loc"][-1] == field

@allure.title("API Post Booking - Large Input")
@allure.description("Verify that the API returns a 422 error when fields in the booking creation request have excessively large values that exceed validation limits")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.post
@pytest.mark.parametrize("field, value, detail_type", 
                         [
                             ("first_name", "a"*1000, "string_too_long"),
                             ("last_name", "a"*1000, "string_too_long"),
                             ("total_price", 1_000_001, "less_than_equal")
                         ],
                         ids=["first_name", "last_name", "total_price"])
def test_large_input_status_422(booking_service, booking_data, field, value, detail_type):
    booking_data[field] = value

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422

    fail_response_data = response.json()
    assert fail_response_data["detail"][0]["type"] == detail_type
    assert fail_response_data["detail"][0]["loc"][-1] == field

@allure.title("API Post Booking - Empty Field Value")
@allure.description("Verify that the API returns a 422 error when fields in the booking creation request are empty")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.post
@pytest.mark.parametrize("field, value, detail_type", 
                         [
                             ("first_name", "", "string_too_short"),
                             ("last_name", "", "string_too_short"),
                             ("total_price", "", "int_parsing")
                         ],
                         ids=["first_name", "last_name", "total_price"])
def test_empty_field_status_422(booking_service, booking_data, field, value, detail_type):
    booking_data[field] = value

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422
    fail_response_data = response.json()
    assert fail_response_data["detail"][0]["type"] == detail_type
    assert fail_response_data["detail"][0]["loc"][-1] == field

@allure.title("API Post Booking - Special Characters")
@allure.description("Verify that the API returns a 422 error when string fields in the booking creation request contain special characters that violate validation rules")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.post
@pytest.mark.parametrize("field, value, detail_type", 
                         [
                             ("first_name", "<script>", "value_error"),
                             ("last_name", "SELECT *", "value_error")
                         ],
                         ids=["first_name", "last_name"])
def test_special_chars_status_422(booking_service, booking_data, field, value, detail_type):
    booking_data[field] = value

    response = booking_service.create_booking(booking_data)

    assert response.status_code == 422

    fail_response_data = response.json()
    assert fail_response_data["detail"][0]["type"] == detail_type
    assert fail_response_data["detail"][0]["loc"][-1] == field