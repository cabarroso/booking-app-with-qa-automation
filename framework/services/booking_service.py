import requests
import logging
import time
from datetime import datetime
import uuid

logger = logging.getLogger("booking_service")

BASE_URL = "http://localhost:8000"

class BookingService:

    def create_booking(self, data):
        request_id = str(uuid.uuid4())[:8]
        logger.info(f"[req: {request_id}] REQUEST POST /bookings")
        logger.info(f"[req: {request_id}] PAYLOAD: {data}")
                    
        start = time.time()
        response = requests.post(f"{BASE_URL}/bookings", json=data)
        try:
            response_body = response.json()
        except Exception:
            response_body = response.text
        duration = time.time() - start
            

        if (response.status_code >= 400):
            logger.error(f"[req: {request_id}] RESPONSE POST /bookings | {response.status_code} | {duration:.3f}s")
            logger.error(f"[req: {request_id}] RESPONSE BODY: {str(response_body)[:500]}")

        else:
            logger.info(f"[req: {request_id}] RESPONSE POST /bookings | {response.status_code} | {duration:.3f}s")
            logger.info(f"[req: {request_id}] RESPONSE BODY: {str(response_body)[:500]}")

        return response

    def get_bookings(self):
        request_id = str(uuid.uuid4())[:8]

        start = time.time()
        response = requests.get(f"{BASE_URL}/bookings")
        try:
            response_body = response.json()
        except Exception:
            response_body = response.text
        duration = time.time() - start

        if (response.status_code >= 400):
            logger.error(f"[req: {request_id}] RESPONSE GET /bookings | {response.status_code} | {duration:.3f}s")
            logger.error(f"[req: {request_id}] RESPONSE BODY: {str(response_body)[:500]}")

        else:
            logger.info(f"[req: {request_id}] RESPONSE GET /bookings | {response.status_code} | {duration:.3f}s")
            logger.info(f"[req: {request_id}] RESPONSE BODY: {str(response_body)[:500]}")

        return response
    
    def get_booking(self, booking_id):
        request_id = str(uuid.uuid4())[:8]

        start = time.time()
        response = requests.get(f"{BASE_URL}/bookings/{booking_id}")
        try:
            response_body = response.json()
        except Exception:
            response_body = response.text
        duration = time.time() - start

        if (response.status_code >= 400):
            logger.error(f"[req: {request_id}] RESPONSE GET /bookings/{booking_id} | {response.status_code} | {duration:.3f}s")
            logger.error(f"[req: {request_id}] RESPONSE BODY: {str(response_body)[:500]}")

        else:
            logger.info(f"[req: {request_id}] RESPONSE GET /bookings/{booking_id} | {response.status_code} | {duration:.3f}s")
            logger.info(f"[req: {request_id}] RESPONSE BODY: {str(response_body)[:500]}")

        return response