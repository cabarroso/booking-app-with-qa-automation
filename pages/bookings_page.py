from playwright.sync_api import Locator, Page

class BookingsPage():
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://localhost:5173/bookings"

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
    def last_booking_first_name_locator(self) -> Locator:
        return self.last_booking_row_locator.locator(".first-name")
    
    @property
    def last_booking_last_name_locator(self) -> Locator:
        return self.last_booking_row_locator.locator(".last-name")
    
    @property
    def last_booking_total_price_locator(self) -> Locator:
        return self.last_booking_row_locator.locator(".total-price")
    
    def open(self):
        self.page.goto(self.base_url)

    def get_last_booking_first_name(self) -> str:
        return self.last_booking_first_name_locator.inner_text()
    
    def get_last_booking_last_name(self) -> str:
        return self.last_booking_last_name_locator.inner_text()
    
    def get_last_booking_total_price(self) -> int:
        return int(self.last_booking_total_price_locator.inner_text())
        
