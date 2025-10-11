from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import ReviewViewSet, SpotViewSet

router = DefaultRouter()
router.register(r"spots", SpotViewSet, basename="spot")
router.register(r"reviews", ReviewViewSet, basename="review")
urlpatterns = [
    path("", include(router.urls)),
]
