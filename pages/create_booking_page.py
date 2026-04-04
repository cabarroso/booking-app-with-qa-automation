from playwright.sync_api import Locator, Page

class CreateBookingPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://localhost:5173/create"
    
    @property
    def current_url(self) -> str:
        return self.page.url

    @property
    def heading_locator(self) -> Locator:
        return self.page.get_by_role("heading", name="Create Booking")
    
    @property
    def first_name_input_locator(self) -> Locator:
        return self.page.get_by_role("textbox", name="First Name")
    
    @property
    def last_name_input_locator(self) -> Locator:
        return self.page.get_by_role("textbox", name="Last Name")
    
    @property
    def total_price_input_locator(self) -> Locator:
        return self.page.get_by_role("spinbutton", name="Total Price")
    
    @property
    def deposit_paid_input_locator(self) -> Locator:
        return self.page.get_by_role("checkbox", name="Deposit Paid")
    
    @property
    def check_in_input_locator(self) -> Locator:
        return self.page.get_by_role("textbox", name="Check In")

    @property
    def check_out_input_locator(self) -> Locator:
        return self.page.get_by_role("textbox", name="Check Out")

    @property
    def additional_needs_input_locator(self) -> Locator:
        return self.page.get_by_role("textbox", name="Additional Needs")
    
    @property
    def button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Create Booking")

    def open(self):
        self.page.goto(self.base_url)

    def fill_first_name(self, first_name: str):
        self.first_name_input_locator.fill(first_name)

    def fill_last_name(self, last_name: str):
        self.last_name_input_locator.fill(last_name)

    def fill_total_price(self, total_price: int):
        self.total_price_input_locator.fill(total_price)

    def check_deposit_paid(self, deposit_paid: bool):
        self.deposit_paid_input_locator.set_checked(deposit_paid)

    def fill_check_in(self, check_in: str):
        self.check_in_input_locator.fill(check_in)

    def fill_check_out(self, check_out: str):
        self.check_out_input_locator.fill(check_out)

    def fill_additional_needs(self, additional_needs: str):
        self.additional_needs_input_locator.fill(additional_needs)

    def submit(self):
        self.button_locator.click()

    def create_booking(self, booking_data):
        self.fill_first_name(booking_data['first_name'])
        self.fill_last_name(booking_data['last_name'])
        self.fill_total_price(str(booking_data['total_price']))
        self.check_deposit_paid(booking_data['deposit_paid'])
        self.fill_check_in(booking_data['check_in'])
        self.fill_check_out(booking_data['check_out'])
        self.fill_additional_needs(booking_data['additional_needs'])
        self.submit()