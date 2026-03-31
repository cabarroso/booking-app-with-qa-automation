import pytest

@pytest.mark.smoke
@pytest.mark.delete_booking
def test_delete_booking_status(booking_service, last_booking_id):
    response = booking_service.delete_booking(last_booking_id)

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