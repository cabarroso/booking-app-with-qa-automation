from faker import Faker
import random

fake = Faker()

def generate_booking_data():
    check_in_date = fake.date_between(start_date="today", end_date="+30d")
    check_out_date = fake.date_between(start_date=check_in_date, end_date="+60d")

    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "total_price": random.randint(50, 500),
        "deposit_paid": random.choice([True, False]),
        "check_in": str(check_in_date),
        "check_out": str(check_out_date),
        "additional_needs": fake.word()
    }