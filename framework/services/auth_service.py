import requests
import logging
import time
import uuid

from config import API_BASE_URL

logger = logging.getLogger("auth_service")

class AuthService:

    def _request(self, method, endpoint, **kwargs):
        request_id = str(uuid.uuid4())[:8]

        logger.info(f"[req: {request_id}] REQUEST {method} {endpoint}")
        booking_data = kwargs.get("json")
        if booking_data:
            logger.info(f"[req: {request_id}] PAYLOAD: {booking_data}")

        start = time.time()
        response = requests.request(method, f"{API_BASE_URL}{endpoint}", json=booking_data)
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
    
    def login(self, login_credentials):
        return self._request("POST", "/auth/login", json=login_credentials)
      