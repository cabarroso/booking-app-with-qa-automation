import requests

BASE_URL = "http://localhost:8000"

class BookingService:

    def create_booking(self, data):
        response = requests.post(f"{BASE_URL}/bookings", json=data)
        return response
