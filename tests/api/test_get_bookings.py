import pytest

from framework.utils.helpers import assert_booking_data_matches

@pytest.mark.get
@pytest.mark.bookings
@pytest.mark.api
@pytest.mark.smoke
def test_get_bookings_returns_list(booking_service):
    response = booking_service.get_bookings()
    assert response.status_code == 200

    bookings = response.json()
    assert isinstance(bookings, list)

@pytest.mark.get
@pytest.mark.bookings
@pytest.mark.api
@pytest.mark.smoke
def test_get_bookings_includes_created_booking(created_booking, booking_service):
    new_booking = created_booking["response_data"]

    response = booking_service.get_bookings()
    assert response.status_code == 200

    bookings = response.json()
    assert any(booking["id"] == new_booking["id"] for booking in bookings)

@pytest.mark.get
@pytest.mark.bookings
@pytest.mark.api
@pytest.mark.smoke
def test_get_bookings_has_unique_ids(three_created_bookings):
    ids = [booking["id"] for booking in three_created_bookings]
    assert len(ids) == len(set(ids))

@pytest.mark.get
@pytest.mark.bookings
@pytest.mark.api
@pytest.mark.smoke
def test_get_bookings_matches_get_booking_data(created_booking, booking_service):
    new_booking = created_booking["response_data"]

    # Get all bookings
    response = booking_service.get_bookings()
    assert response.status_code == 200

    bookings = response.json()
    matching_bookings = [booking for booking in bookings if booking["id"] == new_booking["id"]]

    booking_in_list = matching_bookings[0]
    assert_booking_data_matches(booking_in_list, new_booking)

# @pytest.mark.get
# @pytest.mark.bookings
# @pytest.mark.api
# @pytest.mark.smoke
# def test_get_bookings_while_empty(created_booking, booking_service, validate_booking):
#     # MUST IMPLEMENT LAST
#     pass 

    
    
