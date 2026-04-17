# helper function to compare and assert booking data matches
def assert_booking_data_matches(booking_data1, booking_data2):
    assert booking_data1["first_name"] == booking_data2["first_name"]
    assert booking_data1["last_name"] == booking_data2["last_name"]
    assert booking_data1["total_price"] == booking_data2["total_price"]
    assert booking_data1["deposit_paid"] == booking_data2["deposit_paid"]
    assert booking_data1["check_in"] == booking_data2["check_in"]
    assert booking_data1["check_out"] == booking_data2["check_out"]
    assert booking_data1["additional_needs"] == booking_data2["additional_needs"]