import pytest

from framework.services.booking_service import BookingService
from framework.utils.data_generator import generate_booking_data

@pytest.fixture
def booking_service() -> BookingService:
    return BookingService()

@pytest.fixture
def booking_data():
    return generate_booking_data()