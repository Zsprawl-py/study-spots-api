from uuid import UUID

from django.core.management.base import BaseCommand

from spots.models import Spot

SEED = [
    ("11111111-1111-1111-1111-111111111111","Biblioteca Civica Centrale","Via della Cittadella 5",45.0705,7.6869,5,True,True),
    ("22222222-2222-2222-2222-222222222222","Biblioteca Luigi Einaudi (BLE)","Lungo Dora Siena 100/A",45.0813,7.6929,4,True,True),
    ("33333333-3333-3333-3333-333333333333","Biblioteca Politecnico di Torino","Corso Duca degli Abruzzi 24",45.0625,7.6629,4,True,True),
]

class Command(BaseCommand):
    help = 'Seed the database with demo spots'

    def handle(self, *args, **kwargs):
        created = 0
        for pk, name, addr, lat, lng, quiet, wifi, outlets in SEED:
            obj, was_created = Spot.objects.get_or_create(
                pk=UUID(pk),
                defaults=dict(name=name, address=addr, city="Torino", lat=lat, lng=lng,
                              quiet_level=quiet, wifi=wifi, outlets=outlets)
            )
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f'Seeded {created} demo spots.'))