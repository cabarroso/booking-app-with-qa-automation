import pytest

@pytest.mark.smoke
@pytest.mark.put_booking
def test_update_booking_status(booking_service, booking_data, last_booking_id):
    response = booking_service.update_booking(last_booking_id, booking_data)
    assert response.status_code == 200

@pytest.mark.put_booking
def test_update_booking(booking_service, booking_data, last_booking_id):
    response = booking_service.update_booking(last_booking_id, booking_data)
    updated_booking = response.json()

    assert updated_booking["id"] == last_booking_id
    assert updated_booking["first_name"] == booking_data["first_name"]
    assert updated_booking["last_name"] == booking_data["last_name"]
    assert updated_booking["total_price"] == booking_data["total_price"]
    assert updated_booking["deposit_paid"] == booking_data["deposit_paid"]
    assert updated_booking["check_in"] == booking_data["check_in"]
    assert updated_booking["check_out"] == booking_data["check_out"]
    assert updated_booking["additional_needs"] == booking_data["additional_needs"]

@pytest.mark.put_booking
def test_update_booking_id_doesnt_exist(booking_service, booking_data, last_booking_id):
    response = booking_service.update_booking(last_booking_id + 1, booking_data)

    assert response.status_code >= 400

@pytest.mark.put_booking
@pytest.mark.parametrize("field", ["first_name", "total_price", "check_in"])
def test_update_booking_missing_field(booking_service, booking_data, last_booking_id, field):
    del booking_data[field]

    response = booking_service.update_booking(last_booking_id, booking_data)

    assert response.status_code == 422

@pytest.mark.put_booking
@pytest.mark.parametrize("field, value", 
                        [("first_name", 1337),
                         ("total_price", "fifty dollars"),
                         ("check_in", 3.14),
                         ("deposit_paid", "notabool")],
                        ids=["first_name", "total_price", "check_in", "deposit_paid"])
def test_update_booking_invalid_value_type(booking_service, booking_data, last_booking_id, field, value):
    booking_data[field] = value

    response = booking_service.update_booking(last_booking_id, booking_data)

    assert response.status_code == 422
