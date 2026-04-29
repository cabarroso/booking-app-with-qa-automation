import pytest
import allure

from framework.utils.helpers import assert_booking_data_matches

@allure.title("Get Bookings - Returns List")
@allure.description("Verify that the API returns a list")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.bookings
@pytest.mark.get
def test_get_bookings_returns_list(booking_service):
    with allure.step("GET request to /bookings"):
        response = booking_service.get_bookings()

    with allure.step("Verify response contains status code of 200"):
        assert response.status_code == 200

    bookings = response.json()

    with allure.step("Verify response payload is a list"):
        assert isinstance(bookings, list)

@allure.title("Get Bookings - Includes Newly Created Booking")
@allure.description("Verify that the API includes a newly created booking in the list of bookings")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.api
@pytest.mark.bookings
@pytest.mark.get
@pytest.mark.smoke
def test_get_bookings_includes_created_booking(created_booking, booking_service):
    
    with allure.step("Create a new booking"):
        new_booking = created_booking["response_data"]

    with allure.step("GET request to /bookings"):
        response = booking_service.get_bookings()

    with allure.step("Verify response contains status code of 200"):
        assert response.status_code == 200

    with allure.step("Extract bookings list from response payload"):
        bookings = response.json()

    with allure.step("Grab the new booking from the bookings list by its ID"):
        new_booking_in_list = next((booking for booking in bookings if booking["id"] == new_booking["id"]), None)

    with allure.step("Verify booking uccessfully retrieved from the bookings list"):
        assert new_booking_in_list is not None

    with allure.step("Verify booking data from the bookings list matches data from the earlier newly booking"):
        assert_booking_data_matches(new_booking, new_booking_in_list)

@allure.title("Get Bookings - Unique IDs")
@allure.description("Verify that each booking returned by the API has a unique ID")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.bookings
@pytest.mark.get
def test_get_bookings_has_unique_ids(three_created_bookings):
    with allure.step("Make a list of IDs from bookings"):
        ids = [booking["id"] for booking in three_created_bookings]
    
    with allure.step("Verify that there is only one of each ID number in the list"):
        assert len(ids) == len(set(ids))

@allure.title("Get Bookings - Matches Get_Booking Data")
@allure.description("Verify that the booking data returned by the API matches the data of a newly created booking")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.bookings
@pytest.mark.get
def test_get_bookings_matches_get_booking_data(created_booking, booking_service):

    with allure.step("Create a new booking"):
        new_booking = created_booking["response_data"]

    with allure.step("GET request to /bookings"):
        # Get all bookings
        response = booking_service.get_bookings()

    with allure.step("Verify response contains status code of 200"):
        assert response.status_code == 200

    with allure.step("Extract bookings list from response payload"):
        bookings = response.json()

    with allure.step("Retrieve the new booking from bookings by ID"):
        matching_bookings = [booking for booking in bookings if booking["id"] == new_booking["id"]]
        booking_in_list = matching_bookings[0]

    with allure.step("Get new booking data by GET request to /bookings/{id}"):
        get_response  = booking_service.get_booking(new_booking["id"])

    get_new_booking_data = get_response.json()

    with allure.step("Verify booking data retrieved from bookings matches the data retrieved from GET to /bookings/{id}"):
        assert_booking_data_matches(booking_in_list, get_new_booking_data)

# @allure.title("Get Bookings - When No Bookings Exist")
# @allure.description("Verify that the API returns an empty list when no bookings exist")
# @allure.severity(allure.severity_level.MINOR)
# @pytest.mark.api
# @pytest.mark.booking
# @pytest.mark.bookings
# @pytest.mark.get
# @pytest.mark.smoke
# @pytest.mark.isolated
# def test_get_bookings_when_no_bookings_exist(booking_service):
#     # First, delete all existing bookings
#     response = booking_service.get_bookings()
#     assert response.status_code == 200

#     bookings = response.json()
#     for booking in bookings:
#         del_response = booking_service.delete_booking(booking["id"])
#         assert del_response.status_code in [204, 404]

#     # Now get bookings again
#     response = booking_service.get_bookings()
#     assert response.status_code == 200

#     bookings = response.json()
#     assert isinstance(bookings, list)
#     assert len(bookings) == 0

    
    
