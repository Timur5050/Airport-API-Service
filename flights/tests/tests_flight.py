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


class TestAuthenticatedUserFlight(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test",
            "test123@gmail.com",
            "test123"
        )
        self.client.force_authenticate(self.user)
        self.airport1 = create_default_airport(1)
        self.airport2 = create_default_airport(2)
        self.airplane_type = create_default_airplane_type()
        self.airplane = create_default_airplane(self.airplane_type)
        self.route1 = create_default_route(self.airport1, self.airport2)

    def test_list_flight(self):
        res = self.client.get(flight_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data.get("results")), 0)

        create_default_flight(self.route1, self.airplane)
        res = self.client.get(flight_url)
        self.assertEqual(len(res.data.get("results")), 1)

    def test_retrieve_flight_details(self):
        flight = create_default_flight(self.route1, self.airplane)

        url = detail_url(flight.id)
        res = self.client.get(url)

        serializer = FLightRetrieveSerializer(flight)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res.data.pop("available_places")
        self.assertEqual(res.data, serializer.data)

    def test_create_flight_forbidden(self):
        data = {
            "route": self.route1,
            "airplane": self.airplane,
            "departure_time": datetime.datetime.now(),
            "arrival_time": datetime.datetime.now()
        }

        res = self.client.post(flight_url, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
