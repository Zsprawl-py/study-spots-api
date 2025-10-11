from django.db.models import Avg
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .api_filters import SpotFilter
from .api_permissions import IsAdminOrOwner
from .api_serializers import SpotDetailSerializer, SpotListSerializer
from .api_serializers_reviews import ReviewSerializer
from .models import Review, Spot


class SpotViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    filterset_class = SpotFilter
    search_fields = ["name", "address", "city"]
    ordering_fields = ["name", "created_at", "avg_rating", "quiet_level"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Spot.objects.all().annotate(avg_rating=Avg("reviews__rating")).order_by("-created_at")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SpotDetailSerializer
        return SpotListSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search by name, address, or city",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="wifi",
                description="Filter by wifi availability (true/false)",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="outlets",
                description="Filter by outlets availability (true/false)",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="quiet_min", description="Minimum quiet level (1-5)", required=False, type=int
            ),
            OpenApiParameter(
                name="min_rating",
                description="Minimum average rating (1.0-5.0)",
                required=False,
                type=float,
            ),
            OpenApiParameter(
                name="ordering",
                description="created_at,-created_at, avg_rating,-avg_rating, name,-name, quiet_level,-quiet_level",
                required=False,
                type=str,
            ),
        ],
        responses={200: SpotListSerializer(many=True)},
        description="List study spots with filters, search, ordering, and pagination.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="List or create your review for this spot. GET is public and paginated; POST requires JWT and upserts your review.",
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order reviews by created_at or rating (prefix with '-' for desc).",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="page", description="Page number (1-based).", required=False, type=int
            ),
        ],
        responses={
            200: OpenApiResponse(description="Paginated list of reviews"),
            201: ReviewSerializer,
        },
    )
    @action(detail=True, methods=["get", "post"], url_path="reviews")
    def reviews(self, request, pk=None):
        spot = self.get_object()
        if request.method.lower() == "get":
            qs = spot.reviews.select_related("user").order_by("-created_at")
            # allow ordering override (?ordering=rating or created_at)
            ordering = request.query_params.get("ordering")
            if ordering:
                allowed = {"rating", "-rating", "created_at", "-created_at"}
                if ordering in allowed:
                    qs = qs.order_by(ordering)

            page = self.paginate_queryset(qs)
            if page is not None:
                serializer = ReviewSerializer(
                    page, many=True, context=self.get_serializer_context()
                )
                return self.get_paginated_response(serializer.data)
            serializer = ReviewSerializer(qs, many=True, context=self.get_serializer_context())
            return Response(serializer.data)

        # POST branch: create/update review
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        self.throttle_scope = "review-create"
        self.check_throttles(request)

        data = request.data.copy()
        rating = data.get("rating")
        if rating is None:
            return Response({"detail": "Rating is required."}, status=400)

        review, created = Review.objects.get_or_create(
            spot=spot, user=request.user, defaults={"rating": rating}
        )
        serializer = ReviewSerializer(
            review, data=data, partial=True, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class ReviewViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Review.objects.select_related("spot", "user").all().order_by("-created_at")
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrOwner]
