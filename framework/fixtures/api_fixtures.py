from typing import Generator

import pytest

from framework.services.booking_service import BookingService
from framework.utils.data_generator import generate_booking_data
from framework.services.auth_service import AuthService
from tests.hybrid.test_booking_hybrid import assert_booking_data_matches

@pytest.fixture
def booking_service() -> BookingService:
    return BookingService()

@pytest.fixture
def booking_data():
    return generate_booking_data()

@pytest.fixture
def bookings_response(booking_service: BookingService):
    return booking_service.get_bookings()

@pytest.fixture
def bookings(bookings_response) -> list:
    return bookings_response.json()

@pytest.fixture
def last_booking_id(bookings: list) -> int:
    return bookings[-1]["id"]

@pytest.fixture
def auth_service() -> AuthService:
    return AuthService()

@pytest.fixture
def valid_login_credentials():
    return {
        "username": "admin",
        "password": "password123"
    }

@pytest.fixture
def new_booking(booking_service: BookingService, booking_data: dict, validate_booking) -> Generator[dict, None, None]:
    # Create booking via API
    response = booking_service.create_booking(booking_data)

    # Verify API response and data matches what we sent
    assert response.status_code == 201
    new_booking = response.json()
    assert_booking_data_matches(booking_data, new_booking)

    # Validate response against schema
    validate_booking(new_booking)

    # Log creation for CI visibility
    print(f"[STEP] Created booking ID={new_booking["id"]}")

    yield new_booking

    # Cleanup
    cleanup_response = booking_service.delete_booking(new_booking["id"])
    if cleanup_response.status_code not in [204, 404]:
        raise Exception("Cleanup failed")
    # log cleanup for CI visibility
    print(f"[STEP] Cleaned up booking ID={new_booking["id"]}")