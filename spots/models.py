from django.db import models
import uuid
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify



class Spot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=False, null=False)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, default='Torino')
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)  
    wifi = models.BooleanField(default=True)
    outlets = models.BooleanField(default=True)
    quiet_level = models.PositiveSmallIntegerField(default=3)  # Scale of 1-5
    opening_hours = models.JSONField(null=True, blank=True)  # Store as JSON
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # mimic auto_now on every save
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spot = models.ForeignKey(Spot, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="spot_reviews", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=3)  # Scale of 1-5
    comment = models.TextField(null=True, blank=True)
    visit_date = models.DateField(null=True, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('spot', 'user')  # One review per user per spot
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} -> {self.spot} [{self.rating}]'