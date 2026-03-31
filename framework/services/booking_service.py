import requests
import logging
import time
import uuid

logger = logging.getLogger("booking_service")

BASE_URL = "http://localhost:8000"

class BookingService:

    def _request(self, method, endpoint, **kwargs):
        request_id = str(uuid.uuid4())[:8]

        logger.info(f"[req: {request_id}] REQUEST {method} {endpoint}")
        booking_data = kwargs.get("json")
        if booking_data:
            logger.info(f"[req: {request_id}] PAYLOAD: {booking_data}")

        start = time.time()
        response = requests.request(method, f"{BASE_URL}{endpoint}", json=booking_data)
        try:
            response_body = response.json()
        except Exception:
            response_body = response.text
        duration = time.time() - start

        if (response.status_code >= 400):
            logger.error(f"[req: {request_id}] RESPONSE {method} {endpoint} | {response.status_code} | {duration:.3f}s")
            logger.error(f"[req: {request_id}] RESPONSE BODY: {str(response_body)[:500]}")

        else:
            logger.info(f"[req: {request_id}] RESPONSE {method} {endpoint} | {response.status_code} | {duration:.3f}s")
            logger.info(f"[req: {request_id}] RESPONSE BODY: {str(response_body)[:500]}")

        return response
        
    def get_bookings(self):
        return self._request("GET", "/bookings")
        
    def get_booking(self, booking_id):
        return self._request("GET", f"/bookings/{booking_id}")
    
    def create_booking(self, data):
        return self._request("POST", "/bookings", json=data)
    
    def update_booking(self, booking_id, data):
        return self._request("PUT", f"/bookings/{booking_id}", json=data)
    
    def delete_booking(self, booking_id):
        return self._request("DELETE", f"/bookings/{booking_id}")
        