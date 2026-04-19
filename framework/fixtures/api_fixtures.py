from typing import Generator

import pytest

from framework.services.booking_service import BookingService
from framework.utils.data_generator import generate_booking_data
from framework.services.auth_service import AuthService


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
def created_booking(booking_service: BookingService, booking_data: dict) -> Generator[dict, None, None]:
    # Create booking via API
    response = booking_service.create_booking(booking_data)

    if response.status_code != 201:
        pytest.fail(f"Booking creation failed with status code {response.status_code}")

    # Log creation for CI visibility
    new_booking = response.json()
    print(f"[SETUP] Created booking ID={new_booking['id']}")

    yield {
        "request_data": booking_data,
        "response_data": new_booking
    }

    # Cleanup
    cleanup_response = booking_service.delete_booking(new_booking["id"])
    if cleanup_response.status_code not in [204, 404]:
        pytest.fail(f"Cleanup failed for booking ID={new_booking['id']} with status code {cleanup_response.status_code}")
    # log cleanup for CI visibility
    print(f"[TEARDOWN] Deleted booking ID={new_booking['id']}")