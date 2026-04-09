from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import booking_routes, auth_routes

from app.models.booking import Booking

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allows OPTIONS, POST, etc.
    allow_headers=["*"],
)

# create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)

app.include_router(booking_routes.router)

@app.get("/")
def root():
    return {"message": "Booking API running"}