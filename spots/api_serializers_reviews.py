from rest_framework import serializers
from .models import Review  

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'spot', 'user', 'rating', 'comment', 'visit_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'spot']

        def validate_rating(self, value):
            if not (1 <= value <= 5):
                raise serializers.ValidationError("Rating must be between 1 and 5.")
            return value