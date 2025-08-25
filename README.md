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
