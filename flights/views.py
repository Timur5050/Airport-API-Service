from flights.models import Airport, Crew, Route, Airplane, AirplaneType
from flights.serializers import (
    AirportSerializer,
    CrewSerializer,
    RouteSerializer,
    RouteListSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    AirplaneSerializer
)

from rest_framework.viewsets import ModelViewSet


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


