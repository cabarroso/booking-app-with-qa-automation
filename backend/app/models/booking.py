from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Booking(Base):

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    total_price = Column(Integer, nullable=False)
    deposit_paid = Column(Boolean, nullable=False)

    check_in = Column(String, nullable=False)
    check_out = Column(String, nullable=False)

    additional_needs = Column(String, nullable=False)