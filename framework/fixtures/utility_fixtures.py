import pytest
import json
from jsonschema import validate, ValidationError

@pytest.fixture(scope="session")
def booking_schema():
    with open('tests/schemas/booking_schema.json', 'r') as f:
        booking_schema = json.load(f)
        yield booking_schema
        f.close()

@pytest.fixture
def validate_booking(booking_schema):
    def _validate_booking(booking):
        try:
            validate(instance=booking, schema=booking_schema)
        except ValidationError as e:
            pytest.fail(f"JSON Schema validaiton failed: {e.message}")

    return _validate_booking
