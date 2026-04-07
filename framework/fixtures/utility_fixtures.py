import pytest
import json

@pytest.fixture
def booking_schema():
    with open('tests/schemas/booking_schema.json', 'r') as f:
        booking_schema = json.load(f)
        yield booking_schema
        f.close()