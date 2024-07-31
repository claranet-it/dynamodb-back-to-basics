import pytest
from starlette.testclient import TestClient

from app.main import app
from app.schemas.bike import GetAvailableBikesQuery
from app.schemas.booking import CreateBookingCommand, DeleteBookingCommand


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


@pytest.fixture(scope="function")
def create_booking_command():
    def _create_booking_command(
        user_id: str = "601", bike_id: str = "099", booking_date: str = "2024-06-30"
    ) -> CreateBookingCommand:
        return CreateBookingCommand(
            user_id=user_id, bike_id=bike_id, booking_date=booking_date
        )

    return _create_booking_command


@pytest.fixture(scope="function")
def delete_booking_command():
    def _delete_booking_command(
        bike_id: str = "099", booking_id: str = "123"
    ) -> DeleteBookingCommand:
        return DeleteBookingCommand(bike_id=bike_id, booking_id=booking_id)

    return _delete_booking_command


@pytest.fixture(scope="function")
def get_available_bikes_query():
    def _get_available_bikes_query() -> GetAvailableBikesQuery:
        return GetAvailableBikesQuery()

    return _get_available_bikes_query
