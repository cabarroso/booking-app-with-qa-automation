from fastapi import FastAPI
from app.database import Base, engine
from app.routes import booking_routes, auth_routes

from app.models.booking import Booking

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)

app.include_router(booking_routes.router)

@app.get("/")
def root():
    return {"message": "Booking API running"}