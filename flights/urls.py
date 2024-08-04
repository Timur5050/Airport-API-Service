from flights.views import (
    AirportViewSet,
    CrewViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet
)

from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

router.register("airports", AirportViewSet)
router.register("crews", CrewViewSet)
router.register("routes", RouteViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "flights"
