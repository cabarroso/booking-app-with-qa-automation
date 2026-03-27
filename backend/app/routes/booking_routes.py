from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.booking import Booking
from app.schemas.booking_schema import BookingCreate, BookingResponse

router = APIRouter()

# dependency to get db session
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@router.post("/bookings", response_model=BookingResponse, status_code=201)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    new_booking = Booking(
        first_name=booking.first_name,
        last_name=booking.last_name,
        total_price=booking.total_price,
        deposit_paid=booking.deposit_paid,
        check_in=booking.check_in,
        check_out=booking.check_out,
        additional_needs=booking.additional_needs
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

@router.get("/bookings", response_model=List[BookingResponse], status_code=200)
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@router.get("/bookings/{booking_id}", response_model=BookingResponse, status_code=200)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return booking