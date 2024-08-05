import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from flights.models import Airport, AirplaneType, Route, Airplane, Flight, Crew
from flights.serializers import FlightSerializer, FLightRetrieveSerializer

flight_url = reverse("flights:flight-list")


def detail_url(flight_id):
    return reverse("flights:flight-detail", args=[flight_id])


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


def create_default_airplane(airplane_type):
    return Airplane.objects.create(
        name="test",
        rows=20,
        seats_in_row=10,
        airplane_type=airplane_type
    )


def create_default_flight(route, airplane):
    return Flight.objects.create(
        route=route,
        airplane=airplane,
        departure_time=datetime.datetime.now(),
        arrival_time=datetime.datetime.now()
    )


def create_default_crew(val):
    return Crew.objects.create(
        first_name=f"test{val}",
        last_name=f"test{val}",
    )


class TestUnauthenticatedUserFlight(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user(self):
        res = self.client.get(flight_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


