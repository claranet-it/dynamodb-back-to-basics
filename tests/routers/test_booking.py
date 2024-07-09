import pytest

from app.schemas.booking import CreateBookingCommand


def test_get_bookings_for_bike(client):
    response = client.get("/api/booking/bike/001")

    assert response.status_code == 200
    body = response.json()
    assert "bike" in body
    assert "bookings" in body
    assert body.get("bike") is not None
    assert len(body.get("bookings")) == 4


def test_get_bookings_for_non_existing_bike(client):
    response = client.get("/api/booking/bike/asdf")

    assert response.status_code == 404
    assert response.json() == {"detail": "Bike not found"}


@pytest.mark.parametrize(
    "url, expected_status_code, expected_items_length, expected_next",
    [
        ("/api/booking/user/203", 200, 4, None),
        ("/api/booking/user/asdf", 200, 0, None),
        (
            "/api/booking/user/203?limit=2",
            200,
            2,
            "eyJzayI6ICJCT09LSU5HIzAwNiIsICJnc2kxX3BrIjogIlVTRVIjMjAzIiwgInBrIjogIkJJS0UjMDAyIiwgImdzaTFfc2siOiAiQk9PS0lORyMwMDYifQ==",
        ),
        (
            "/api/booking/user/203?limit=2&start=eyJzayI6ICJCT09LSU5HIzAxMiIsICJnc2kxX3BrIjogIlVTRVIjMjAzIiwgInBrIjogIkJJS0UjMDA0IiwgImdzaTFfc2siOiAiQk9PS0lORyMwMTIifQ==",
            200,
            0,
            None,
        ),
    ],
)
def test_get_bookings(
    client, url, expected_status_code, expected_items_length, expected_next
):
    response = client.get(url)

    assert response.status_code == expected_status_code
    body = response.json()
    assert "items" in body
    assert "next" in body
    assert body.get("next") == expected_next
    assert len(body.get("items")) == expected_items_length


@pytest.mark.parametrize(
    "url, expected_status_code, expected_items_length, expected_next",
    [
        ("/api/booking/available-bikes", 200, 3, None),
        (
            "/api/booking/available-bikes?limit=2",
            200,
            2,
            "eyJzayI6ICJCSUtFIzAwMyIsICJnc2kxX3BrIjogIkFWQUlMQUJMRSIsICJwayI6ICJCSUtFIzAwMyIsICJnc2kxX3NrIjogIjAwMyJ9",
        ),
        (
            "/api/booking/available-bikes?start=eyJzayI6ICJCSUtFIzAwMyIsICJnc2kxX3BrIjogIkFWQUlMQUJMRSIsICJwayI6ICJCSUtFIzAwMyIsICJnc2kxX3NrIjogIjAwMyJ9",
            200,
            1,
            None,
        ),
    ],
)
def test_get_available_bikes(
    client, url, expected_status_code, expected_items_length, expected_next
):
    response = client.get(url)

    assert response.status_code == expected_status_code
    body = response.json()
    assert "items" in body
    assert "next" in body
    assert body.get("next") == expected_next
    assert len(body.get("items")) == expected_items_length


def test_get_booking_detail(client):
    response = client.get("/api/booking/detail/002/014")

    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == "014"
    assert body.get("userId") == "201"
    assert body.get("bikeId") == "002"
    assert body.get("bookingDate") == "2024-06-30"


def test_get_booking_detail_for_non_existing_booking(client):
    response = client.get("/api/booking/detail/002/asdf")

    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found"}


def test_create_booking(client):
    response = client.post(
        "/api/booking",
        json={
            "userId": "601",
            "bikeId": "099",
            "bookingDate": "2024-06-30",
        },
    )

    assert response.status_code == 201
    body = response.json()

    booking_id = body.get("id")
    user_id = body.get("userId")
    bike_id = body.get("bikeId")
    assert booking_id is not None
    assert user_id == "601"
    assert bike_id == "099"
    assert body.get("bookingDate") == "2024-06-30"


def test_delete_booking(client, create_booking):
    bike_id = "099"
    booking_id = create_booking(
        CreateBookingCommand(user_id="601", bike_id=bike_id, booking_date="2024-06-30")
    )

    response = client.delete(f"/api/booking/{bike_id}/{booking_id}")

    assert response.status_code == 204


def test_delete_non_existing_booking(client):
    response = client.delete("/api/booking/001/asdf")

    assert response.status_code == 404
