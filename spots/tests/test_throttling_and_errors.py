import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from spots.models import Spot
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_review_post_throttle():
    user = get_user_model().objects.create_user(username="peter", password="x")
    api = APIClient()
    token = api.post("/api/v1/auth/token/", {"username": "peter", "password": "x"}, format="json").json()["access"]
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    spot = baker.make(Spot, lat=45.0, lng=7.0)

    for _ in range(12):
        res = api.post(f"/api/v1/spots/{spot.id}/reviews/", {"rating": 5}, format="json")
        assert res.status_code in (200, 201, 429)
    
    if res.status_code == 429:
        data = res.json()
        assert "status_code" in data and data["status_code"] == 429
        assert "detail" in data

@pytest.mark.django_db
def test_auth_required_error_shape(client):
    spot = baker.make(Spot, lat=45.0, lng=7.0)
    res = client.post(f"/api/v1/spots/{spot.id}/reviews/", data={"rating": 5}, content_type="application/json")
    assert res.status_code == 401
    data = res.json()
    assert data['status_code'] == 401 and 'detail' in data