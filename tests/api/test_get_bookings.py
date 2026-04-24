import pytest

from framework.utils.helpers import assert_booking_data_matches

@pytest.mark.api
@pytest.mark.booking
@pytest.mark.bookings
@pytest.mark.get
def test_get_bookings_returns_list(booking_service):
    response = booking_service.get_bookings()
    assert response.status_code == 200

    bookings = response.json()
    assert isinstance(bookings, list)

@pytest.mark.api
@pytest.mark.booking
@pytest.mark.bookings
@pytest.mark.get
@pytest.mark.smoke
def test_get_bookings_includes_created_booking(created_booking, booking_service):
    new_booking = created_booking["response_data"]

    response = booking_service.get_bookings()
    assert response.status_code == 200

    bookings = response.json()
    new_booking_in_list = next((booking for booking in bookings if booking["id"] == new_booking["id"]), None)

    assert new_booking_in_list is not None
    assert_booking_data_matches(new_booking, new_booking_in_list)

@pytest.mark.api
@pytest.mark.booking
@pytest.mark.bookings
@pytest.mark.get
def test_get_bookings_has_unique_ids(three_created_bookings):
    ids = [booking["id"] for booking in three_created_bookings]
    assert len(ids) == len(set(ids))

@pytest.mark.api
@pytest.mark.booking
@pytest.mark.bookings
@pytest.mark.get
def test_get_bookings_matches_get_booking_data(created_booking, booking_service):
    new_booking = created_booking["response_data"]

    # Get all bookings
    response = booking_service.get_bookings()
    assert response.status_code == 200

    bookings = response.json()
    matching_bookings = [booking for booking in bookings if booking["id"] == new_booking["id"]]

    booking_in_list = matching_bookings[0]
    assert_booking_data_matches(booking_in_list, new_booking)

@pytest.mark.api
@pytest.mark.booking
@pytest.mark.bookings
@pytest.mark.get
@pytest.mark.smoke
def test_get_bookings_when_no_bookings_exist(booking_service):
    # First, delete all existing bookings
    response = booking_service.get_bookings()
    assert response.status_code == 200

    bookings = response.json()
    for booking in bookings:
        del_response = booking_service.delete_booking(booking["id"])
        assert del_response.status_code in [204, 404]

    # Now get bookings again
    response = booking_service.get_bookings()
    assert response.status_code == 200

    bookings = response.json()
    assert isinstance(bookings, list)
    assert len(bookings) == 0

    
    
