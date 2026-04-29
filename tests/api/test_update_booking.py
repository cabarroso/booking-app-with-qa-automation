import pytest
import allure

from framework.utils.helpers import assert_booking_data_matches

@allure.title("Update Booking - Successfully Update a Newly Created Booking")
@allure.description("Verify that a newly created booking contains updated fields with valid values.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.put
def test_successfully_update_booking(created_booking, booking_service, booking_data, validate_booking):
    
    with allure.step("Create a new booking"):
        new_booking = created_booking["response_data"]

    # MAIN TESTS
    with allure.step("Update new booking with test data"):
        response = booking_service.update_booking(new_booking["id"], booking_data)

    with allure.step("Verify response contains staus code 200"):
        assert response.status_code == 200

    updated_booking = response.json()

    with allure.step("Validate updated booking against Booking schema"):
        validate_booking(updated_booking)

    with allure.step("Verify updated booking and the created booking have same ID"):
        assert updated_booking["id"] == new_booking["id"]

    with allure.step("Get created booking using ID from newly created booking tht was updated"):
        get_response = booking_service.get_booking(new_booking["id"])
        get_response_data = get_response.json()

    with allure.step("Verify the booking data from the GET request matched the test data used to updated the new booking"):
        assert_booking_data_matches(get_response_data, booking_data)


@allure.title("Update Booking - Invalid Booking ID")
@allure.description("Verify that HTML status code 422 is returned when trying to update a booking with an invalid ID (e.g. 0 or negative)")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.put
@pytest.mark.parametrize("booking_id", [0, -1], ids=["zero_id", "negative_id"])
def test_update_invalid_booking_id_returns_422(booking_service, booking_data, booking_id):
    
    with allure.step("Attempt to update a booking with invalid ID (less than 1)"):
        response = booking_service.update_booking(booking_id, booking_data)

    with allure.step("Verify response contains status code of 422"):
        assert response.status_code == 422

    error = response.json()

    with allure.step("Verify error response detail"):
        assert error["detail"][0]["type"] == "greater_than_equal"
        assert error["detail"][0]["loc"][-1] == "booking_id"

@allure.title("Update Booking - Missing Field")
@allure.description("Verify that HTML status of 422 is returned when trying to update a booking with missing required fields")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.put
@pytest.mark.parametrize("field", ["first_name", "total_price", "check_in"])
def test_update_booking_missing_field(created_booking, booking_service, booking_data, field):
    
    with allure.step("Create a new booking"):
        new_booking = created_booking["response_data"]

    # MAIN TESTS
    
    with allure.step("Verify necessary field exists in test data"):
        assert field in booking_data

    with allure.step("Delete field from test data"):
        del booking_data[field]

    with allure.step("Attempt to update new booking with missing field in test data"):
        response = booking_service.update_booking(new_booking["id"], booking_data)

    with allure.step("Verify response contains status code of 422"):
        assert response.status_code == 422

    put_response_data = response.json()

    with allure.step("Verify error response detail"):
        assert put_response_data["detail"][0]["type"] == "missing"
        assert put_response_data["detail"][0]["loc"][-1] == field

@allure.title("Update Booking - Invalid Field Type")
@allure.description("Verify that the API returns a 422 error when fields in the updated data request have invalid data types")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.booking
@pytest.mark.put
@pytest.mark.parametrize("field, value, detail_type", 
                        [("first_name", 1337, "string_type"),
                         ("total_price", "fifty dollars", "int_parsing"),
                         ("check_in", 3.14, "date_from_datetime_inexact"),
                         ("deposit_paid", "notabool", "bool_parsing")],
                        ids=["first_name", "total_price", "check_in", "deposit_paid"])
def test_update_booking_invalid_value_type(created_booking, booking_service, booking_data, field, value, detail_type):
    
    with allure.step("Create a new booking"):
        new_booking = created_booking["response_data"]

    # MAIN TESTS

    with allure.step("Give field in test data a value of invalid type"):
        booking_data[field] = value

    with allure.step("Attempt to update new booking with test data with an invalid value type"):
        response = booking_service.update_booking(new_booking["id"], booking_data)

    with allure.step("Verify response contains error code of 422"):
        assert response.status_code == 422
    
    put_response_data = response.json()

    with allure.step("Verify error response detail"):
        assert put_response_data["detail"][0]["type"] == detail_type
        assert put_response_data["detail"][0]["loc"][-1] == field
