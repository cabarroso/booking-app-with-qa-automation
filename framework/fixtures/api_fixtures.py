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

