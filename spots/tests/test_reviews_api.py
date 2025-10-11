import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from spots.models import Review, Spot


@pytest.mark.django_db
def test_reviews_list_public(client):
    spot = baker.make(Spot, lat=45.0, lng=7.0)
    res = client.get(f"/api/v1/spots/{spot.id}/reviews/")
    assert res.status_code == 200
    assert "results" in res.json()


@pytest.mark.django_db
def test_create_review_requires_auth(client):
    spot = baker.make(Spot, lat=45.0, lng=7.0)
    res = client.post(
        f"/api/v1/spots/{spot.id}/reviews/", data={"rating": 5}, content_type="application/json"
    )
    assert res.status_code == 401


@pytest.mark.django_db
def test_create_and_update_review_with_jwt(django_user_model):
    # create user & get token
    password = "pass12345"
    user = django_user_model.objects.create_user(username="alice", password=password)
    api = APIClient()
    token_res = api.post(
        "/api/v1/auth/token/", {"username": "alice", "password": password}, format="json"
    )
    assert token_res.status_code == 200
    access = token_res.json()["access"]
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    spot = baker.make(Spot, lat=45.0, lng=7.0)

    # create (201)
    res = api.post(
        f"/api/v1/spots/{spot.id}/reviews/", {"rating": 5, "comment": "Great"}, format="json"
    )
    assert res.status_code in (200, 201)
    rid = res.json()["id"]

    # update via /reviews/{id}/ (owner only)
    res2 = api.patch(f"/api/v1/reviews/{rid}/", {"rating": 4}, format="json")
    assert res2.status_code == 200
    assert res2.json()["rating"] == 4


@pytest.mark.django_db
def test_owner_only_delete_review(django_user_model):
    owner = django_user_model.objects.create_user(username="bob", password="x")
    other = django_user_model.objects.create_user(username="eve", password="x")
    spot = baker.make(Spot, lat=45.0, lng=7.0)
    rev = Review.objects.create(spot=spot, user=owner, rating=5)

    api = APIClient()
    # login as other
    t = api.post("/api/v1/auth/token/", {"username": "eve", "password": "x"}, format="json")
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {t.json()['access']}")
    forbidden = api.delete(f"/api/v1/reviews/{rev.id}/")
    assert forbidden.status_code in (403, 404)  # permission denied

    # login as owner
    api = APIClient()
    t2 = api.post("/api/v1/auth/token/", {"username": "bob", "password": "x"}, format="json")
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {t2.json()['access']}")
    ok = api.delete(f"/api/v1/reviews/{rev.id}/")
    assert ok.status_code == 204
