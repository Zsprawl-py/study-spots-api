from rest_framework import serializers

from .models import Spot


class SpotListSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(
        read_only=True, help_text="Average user rating 1.0–5.0 (null if no reviews)"
    )

    class Meta:
        model = Spot
        fields = [
            "id",
            "name",
            "address",
            "city",
            "lat",
            "lng",
            "wifi",
            "outlets",
            "quiet_level",
            "average_rating",
            "created_at",
            "opening_hours",
        ]


class SpotDetailSerializer(SpotListSerializer):
    class Meta(SpotListSerializer.Meta):
        fields = SpotListSerializer.Meta.fields + ["updated_at"]
