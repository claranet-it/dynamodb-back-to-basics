import pytest
from starlette.testclient import TestClient

from app.main import app
from app.schemas.booking import CreateBookingCommand


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def create_booking(client: TestClient):
    def _create_booking(command: CreateBookingCommand) -> str:
        response = client.post(
            "/api/booking",
            json={
                "userId": command.user_id,
                "bikeId": command.bike_id,
                "bookingDate": command.booking_date.strftime("%Y-%m-%d"),
            },
        )

        assert response.status_code == 201
        body = response.json()

        return body.get("id")

    return _create_booking
