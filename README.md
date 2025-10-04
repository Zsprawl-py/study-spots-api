# Torino Study Spots API (Day 1)
Django 5 project for cataloging study spots in Torino.

## Today
- Project bootstrapped
- Models: Spot, Review
- Admin configured
- Seed data loaded

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata spots
python manage.py runserver


## Day 2
- Added DRF, django-filter, drf-spectacular
- Endpoints:
  - GET /api/v1/spots/
  - GET /api/v1/spots/{id}/
- Features: search (?search=), filters (?wifi,&outlets,&city,&quiet_min,&min_rating), ordering (?ordering=), pagination


## Day 3
- JWT auth: POST /api/v1/auth/token/, /api/v1/auth/token/refresh/
- Reviews:
  - GET /api/v1/spots/{id}/reviews/
  - POST /api/v1/spots/{id}/reviews/ (auth, upsert)
  - GET/PATCH/DELETE /api/v1/reviews/{id}/ (owner or admin)
- Throttling: review-create = 10/min; anon=60/min; user=120/min
