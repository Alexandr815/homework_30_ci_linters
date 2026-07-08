import pytest
from main.models import Client, ClientParking, Parking


@pytest.mark.parametrize("url", [
    "/clients",
    "/clients/1"
])
def test_get_routes(client, url):
    resp = client.get(url)
    assert resp.status_code == 200


def test_create_client(client, db):
    resp = client.post("/clients", json={
        "name": "Test",
        "surname": "User"
    })
    assert resp.status_code == 201
    assert db.session.query(Client).count() == 2


def test_create_parking(client, db):
    resp = client.post("/parkings", json={
        "address": "Addr",
        "opened": True,
        "count_places": 5,
        "count_available_places": 5
    })
    assert resp.status_code == 201
    assert db.session.query(Parking).count() == 2


@pytest.mark.parking
def test_enter_parking(client, db):
    resp = client.post("/client_parkings", json={
        "client_id": 1,
        "parking_id": 1
    })

    parking = db.session.get(Parking, 1)

    assert resp.status_code == 200
    assert parking.count_available_places == 9


@pytest.mark.parking
def test_exit_parking(client, db):
    client.post("/client_parkings", json={
        "client_id": 1,
        "parking_id": 1
    })

    resp = client.delete("/client_parkings", json={
        "client_id": 1,
        "parking_id": 1
    })

    parking = db.session.get(Parking, 1)
    cp = db.session.query(ClientParking).first()

    assert resp.status_code == 200
    assert parking.count_available_places == 10
    assert cp.time_out is not None
