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
