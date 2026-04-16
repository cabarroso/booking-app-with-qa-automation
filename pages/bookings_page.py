from playwright.sync_api import Locator, Page, expect

from config import UI_BASE_URL



class BookingsPage():
    def __init__(self, page: Page):
        self.page = page
        self.base_url = f"{UI_BASE_URL}/bookings"

    @property
    def current_url(self) -> str:
        return self.page.url
        
    @property
    def heading_locator(self) -> Locator:
        return self.page.get_by_role("heading", name="Bookings")
    
    @property
    def booking_row_locator(self) -> Locator:
        return self.page.locator(".booking")
    
    @property
    def last_booking_row_locator(self) -> Locator:
        return self.booking_row_locator.last
    
    @property 
    def last_booking_id_locator(self) -> Locator:
        return self.last_booking_row_locator.locator(".booking-id")
    
    @property
    def last_booking_first_name_locator(self) -> Locator:
        return self.last_booking_row_locator.locator(".first-name")
    
    @property
    def last_booking_last_name_locator(self) -> Locator:
        return self.last_booking_row_locator.locator(".last-name")
    
    @property
    def last_booking_total_price_locator(self) -> Locator:
        return self.last_booking_row_locator.locator(".total-price")
    
    @property
    def last_booking_delete_button_locator(self) -> Locator:
        return self.last_booking_row_locator.get_by_role("button", name="Delete")
    
    def open(self):
        self.page.goto(self.base_url)
    
    def reload(self):
        self.page.reload()

    def get_booking_row_by_id(self, booking_id: int) -> Locator:
        return self.page.get_by_test_id(f"booking-row-{booking_id}")
    
    def get_booking_first_name_by_id(self, booking_id: int) -> str:
        return self.get_booking_row_by_id(booking_id).locator(".first-name").inner_text()
    
    def get_booking_last_name_by_id(self, booking_id: int) -> str:
        return self.get_booking_row_by_id(booking_id).locator(".last-name").inner_text()
    
    def get_booking_total_price_by_id(self, booking_id: int) -> int:
        return int(self.get_booking_row_by_id(booking_id).locator(".total-price").inner_text())
    
    def get_booking_deposit_paid_by_id(self, booking_id: int) -> bool:
        return self.get_booking_row_by_id(booking_id).locator(".deposit-paid").inner_text() == "true"
    
    def get_booking_check_in_by_id(self, booking_id: int) -> str:
        return self.get_booking_row_by_id(booking_id).locator(".check-in").inner_text()
    
    def get_booking_check_out_by_id(self, booking_id: int) -> str:
        return self.get_booking_row_by_id(booking_id).locator(".check-out").inner_text()
    
    def get_booking_additional_needs_by_id(self, booking_id: int) -> str:
        return self.get_booking_row_by_id(booking_id).locator(".additional-needs").inner_text()
    
    def get_booking_data_by_id(self, booking_id: int) -> dict:
        return {
            "first_name": self.get_booking_first_name_by_id(booking_id),
            "last_name": self.get_booking_last_name_by_id(booking_id),
            "total_price": self.get_booking_total_price_by_id(booking_id),
            "deposit_paid": self.get_booking_deposit_paid_by_id(booking_id),
            "check_in": self.get_booking_check_in_by_id(booking_id),
            "check_out": self.get_booking_check_out_by_id(booking_id),
            "additional_needs": self.get_booking_additional_needs_by_id(booking_id)
        }

    def get_last_booking_id(self) -> int:
        return int(self.last_booking_id_locator.inner_text())

    def get_last_booking_first_name(self) -> str:
        return self.last_booking_first_name_locator.inner_text()
    
    def get_last_booking_last_name(self) -> str:
        return self.last_booking_last_name_locator.inner_text()
    
    def get_last_booking_total_price(self) -> int:
        return int(self.last_booking_total_price_locator.inner_text())
    
    def delete_last_booking(self):
        self.last_booking_delete_button_locator.click()

    def wait_for_booking(self, booking_id: int, timeout: int = 5000):
        booking_row = self.get_booking_row_by_id(booking_id)
        expect(booking_row).to_be_visible(timeout=timeout)
        
    def booking_row_is_present(self, booking_id: int) -> bool:
        return self.get_booking_row_by_id(booking_id).count() > 0
