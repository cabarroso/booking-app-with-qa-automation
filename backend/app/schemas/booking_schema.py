from pydantic import BaseModel
from typing import Optional

class BookingCreate(BaseModel):
    first_name: str
    last_name: str
    total_price: int
    deposit_paid: bool
    check_in: str
    check_out: str
    additional_needs: Optional[str] = None

class BookingResponse(BookingCreate):
    id: int

    class Config:
        from_attributes = True