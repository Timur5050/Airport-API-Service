import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from flights.models import Airport, AirplaneType, Route, Airplane, Flight, Crew
from flights.serializers import FlightSerializer, FLightRetrieveSerializer

route_url = reverse("flights:route-list")


def detail_url(route_id):
    return reverse("flights:route-detail", args=[route_id])


def create_default_airport(val):
    return Airport.objects.create(
        name=f"test{val}",
        closest_big_city=f"city{val}",
    )


def create_default_airplane_type():
    return AirplaneType.objects.create(
        name="testik"
    )


def create_default_route(source, destination):
    return Route.objects.create(
        source=source,
        destination=destination,
        distance=1000
    )


class TestUnauthenticatedUserRoute(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user(self):
        res = self.client.get(route_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

