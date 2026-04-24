from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

import re

class BookingCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    total_price: int = Field(..., ge=0, le=1_000_000)
    deposit_paid: bool
    check_in: date
    check_out: date
    additional_needs: Optional[str] = Field(default=None, min_length=1, max_length=500)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out < self.check_in:
            raise ValueError("Checkout cannot be before checkin")
        return self
    
    @field_validator("first_name", "last_name")
    def validate_name(cls, value):
        pattern = r"^[A-Za-z\s'-]+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid characters in name")
        return value

class BookingResponse(BookingCreate):
    id: int = Field(..., gt=0)

    class Config:
        from_attributes = True