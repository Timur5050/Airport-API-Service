from django.db.models import F, Count
from rest_framework.pagination import PageNumberPagination

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
    queryset = Route.objects.all().select_related("source", "destination")
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'list':
            serializer_class = RouteListSerializer
        elif self.action == 'create':
            serializer_class = RouteSerializer

        return serializer_class

    def get_queryset(self):
        queryset = self.queryset
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        if source:
            queryset = queryset.filter(source__name__icontains=source)

        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

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

    def get_queryset(self):
        queryset = self.queryset.select_related("airplane_type")
        return queryset


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class FlightViewSet(ModelViewSet):
    queryset = (
        Flight.objects.all()
        .select_related("route", "airplane", "route__source", "route__destination")
        .prefetch_related("crew")
        .annotate(
            available_places=
            F("airplane__rows") * F("airplane__seats_in_row")
            - Count("tickets")
        )
    )
    serializer_class = FlightSerializer
    pagination_class = StandardResultsSetPagination

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

        return queryset


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
