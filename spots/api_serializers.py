from rest_framework import serializers
from .models import Spot

class SpotListSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Spot
        fields = [
            'id', 'name', 'address', 'city', 'lat', 'lng',
            'wifi', 'outlets', 'quiet_level', 'average_rating',
            'created_at', 'opening_hours',
        ]

class SpotDetailSerializer(SpotListSerializer):
    class Meta(SpotListSerializer.Meta):
        fields = SpotListSerializer.Meta.fields + ['updated_at']

        