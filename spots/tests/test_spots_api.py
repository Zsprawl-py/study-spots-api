import pytest
from model_bakery import baker

from spots.models import Review, Spot


@pytest.mark.django_db
def test_list_spots_basic(client):
    baker.make(Spot, _quantity=3, lat=45.0, lng=7.0)
    url = "/api/v1/spots/"
    res = client.get(url)
    assert res.status_code == 200
    data = res.json()
    assert "results" in data and len(data["results"]) >= 3


@pytest.mark.django_db
def test_spots_filter_wifi_and_quiet(client):
    baker.make(Spot, wifi=True, quiet_level=5, _quantity=2, lat=45.0, lng=7.0)
    baker.make(Spot, wifi=False, quiet_level=2, _quantity=1, lat=45.0, lng=7.0)
    res = client.get("/api/v1/spots/?wifi=true&quiet_min=4")
    assert res.status_code == 200
    assert len(res.json()["results"]) == 2


@pytest.mark.django_db
def test_spot_detail(client):
    spot = baker.make(Spot, name="BLE", lat=45.0813, lng=7.6929)
    res = client.get(f"/api/v1/spots/{spot.id}/")
    assert res.status_code == 200
    assert res.json()["name"] == "BLE"


@pytest.mark.django_db
def test_avg_rating_annotation(client, django_user_model):
    user = baker.make(django_user_model)
    spot = baker.make(Spot, lat=45.0, lng=7.0)
    baker.make(Review, spot=spot, user=user, rating=5)
    res = client.get("/api/v1/spots/?min_rating=4")
    assert res.status_code == 200
    ids = [r["id"] for r in res.json()["results"]]
    assert str(spot.id) in ids
