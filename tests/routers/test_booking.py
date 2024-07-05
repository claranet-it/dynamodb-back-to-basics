import pytest


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


@pytest.mark.parametrize(
    "url, expected_status_code, expected_items_length, expected_next",
    [
        ("/api/booking/user/203", 200, 4, None),
        ("/api/booking/user/asdf", 200, 0, None),
        (
            "/api/booking/user/203?limit=2",
            200,
            2,
            "eyJzayI6ICJCT09LSU5HIzAwNiIsICJnczFfcGsiOiAiVVNFUiMyMDMiLCAicGsiOiAiQklLRSMwMDIiLCAiZ3MxX3NrIjogIkJPT0tJTkcjMDA2In0=",
        ),
        (
            "/api/booking/user/203?limit=2&start=eyJzayI6ICJCT09LSU5HIzAxMiIsICJnczFfcGsiOiAiVVNFUiMyMDMiLCAicGsiOiAiQklLRSMwMDQiLCAiZ3MxX3NrIjogIkJPT0tJTkcjMDEyIn0=",
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
            "eyJzayI6ICJCSUtFIzAwMyIsICJnczFfcGsiOiAiQVZBSUxBQkxFIiwgInBrIjogIkJJS0UjMDAzIiwgImdzMV9zayI6ICIwMDMifQ==",
        ),
        (
            "/api/booking/available-bikes?start=eyJzayI6ICJCSUtFIzAwMyIsICJnczFfcGsiOiAiQVZBSUxBQkxFIiwgInBrIjogIkJJS0UjMDAzIiwgImdzMV9zayI6ICIwMDMifQ==",
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
