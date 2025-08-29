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
