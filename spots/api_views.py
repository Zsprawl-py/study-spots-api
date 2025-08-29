from django.db.models import Avg
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Spot
from .api_serializers import SpotListSerializer, SpotDetailSerializer
from .api_filters import SpotFilter

class SpotViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    filterset_class = SpotFilter
    search_fields = ['name', 'address', 'city']
    ordering_fields = ['name', 'created_at', 'avg_rating', 'quiet_level']
    ordering = ['-created_at']

    def get_queryset(self):
        return Spot.objects.all().annotate(avg_rating=Avg('reviews__rating')).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpotDetailSerializer
        return SpotListSerializer