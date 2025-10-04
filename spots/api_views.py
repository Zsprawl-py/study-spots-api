from django.shortcuts import get_object_or_404
from django.db.models import Avg

from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle


from .models import Spot, Review
from .api_permissions import IsAdminOrOwner
from .api_serializers_reviews import ReviewSerializer
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


    @action(detail=True, methods=['get', 'post'], url_path='reviews')
    def reviews(self, request, pk=None):
        spot = self.get_object()
        if request.method.lower() == 'get':
            qs = spot.reviews.select_related('user').order_by('-created_at')
            page = self.paginate_queryset(qs)
            if page is not None:
                serializer = ReviewSerializer(page, many=True, context=self.get_serializer_context())
                return self.get_paginated_response(serializer.data)
            serializer = ReviewSerializer(qs, many=True, context=self.get_serializer_context())
            return Response(serializer.data)

        # --------------------------
        # POST branch: create/update review
        # --------------------------

        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        self.throttle_scope = 'review-create'
        self.check_throttles(request)

        data = request.data.copy()
        rating = data.get('rating')
        if rating is None:
            return Response({'detail': 'Rating is required.'}, status=400)

        review, created = Review.objects.get_or_create(spot=spot, user=request.user, defaults={'rating': rating})
        serializer = ReviewSerializer(review, data=data, partial=True, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    

class ReviewViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.select_related('spot', 'user').all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrOwner]