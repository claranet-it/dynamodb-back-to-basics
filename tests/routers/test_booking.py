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


def test_get_bookings_for_user(client):
    response = client.get("/api/booking/user/203")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert "next" in body
    assert body.get("next") is None
    assert len(body.get("items")) == 4


def test_get_bookings_for_non_existing_user(client):
    response = client.get("/api/booking/user/asdf")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert "next" in body
    assert body.get("next") is None
    assert len(body.get("items")) == 0


def test_get_bookings_for_user_with_limit(client):
    response = client.get("/api/booking/user/203?limit=2")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert "next" in body
    assert (
        body.get("next")
        == "eyJzayI6ICJCT09LSU5HIzAwNiIsICJnczFfcGsiOiAiVVNFUiMyMDMiLCAicGsiOiAiQklLRSMwMDIiLCAiZ3MxX3NrIjogIkJPT0tJTkcjMDA2In0="
    )
    assert len(body.get("items")) == 2
