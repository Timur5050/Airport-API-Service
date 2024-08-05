import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from flights.models import Airport, AirplaneType, Route, Airplane, Flight, Crew
from flights.serializers import FlightSerializer, FLightRetrieveSerializer, RouteSerializer

route_url = reverse("flights:route-list")


def detail_url(route_id):
    return reverse("flights:route-detail", args=[route_id])


def create_default_airport(val):
    return Airport.objects.create(
        name=f"test{val}",
        closest_big_city=f"city{val}",
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


class TestAuthenticatedUserRoute(TestCase):
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



    def test_retrieve_route_details(self):
        route = create_default_route(self.airport1, self.airport2)

        url = detail_url(route.id)
        res = self.client.get(url)

        serializer = RouteSerializer(route)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_route_forbidden(self):
        data = {
            "source": self.airport1.id,
            "destination": self.airport2.id,
            "distance": 1000,
        }

        res = self.client.post(route_url, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TestAdminUserFlight(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin",
            "admin123@gmail.com",
            "admin123"
        )
        self.client.force_authenticate(self.user)
        self.airport1 = create_default_airport(1)
        self.airport2 = create_default_airport(2)

    def test_create_route(self):
        now = timezone.now()
        data = {
            "source": self.airport1.id,
            "destination": self.airport2.id,
            "distance": 1000,
        }

        res = self.client.post(route_url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

