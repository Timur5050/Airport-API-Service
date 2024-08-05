from django.db.models import F, Count

from flights.models import Airport, Crew, Route, Airplane, AirplaneType, Flight, Order
from flights.serializers import (
    AirportSerializer,
    CrewSerializer,
    RouteSerializer,
    RouteListSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    AirplaneSerializer,
    FlightSerializer,
    FlightListSerializer,
    FLightRetrieveSerializer,
    OrderSerializer
)

from rest_framework.viewsets import ModelViewSet


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'list':
            serializer_class = RouteListSerializer
        elif self.action == 'create':
            serializer_class = RouteSerializer

        return serializer_class

    def get_queryset(self):
        queryset = Route.objects.all().select_related("source", "destination")
        return queryset


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'list':
            serializer_class = AirplaneListSerializer
        elif self.action == 'create':
            serializer_class = AirplaneSerializer

        return serializer_class


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'list':
            serializer_class = FlightListSerializer
        elif self.action == "create":
            serializer_class = FlightSerializer
        elif self.action == "retrieve":
            serializer_class = FLightRetrieveSerializer

        return serializer_class

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.annotate(
            available_places=F("airplane__rows") * F("airplane__seats_in_row") - Count("tickets")
        )
        return queryset


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
