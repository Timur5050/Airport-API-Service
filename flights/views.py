from django.db.models import F, Count
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
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


@extend_schema_view(
    list=extend_schema(
        summary="get list of airports",
    ),
    retrieve=extend_schema(
        summary="retrieve airport"
    ),
    update=extend_schema(
        summary="update airport"
    ),
    partial_update=extend_schema(
        summary="partial update airport",
    ),
    create=extend_schema(
        summary="create new airport",
    ),
    destroy=extend_schema(
        summary="delete airport",
    ),
)
class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


@extend_schema_view(
    list=extend_schema(
        summary="get list of crew",
    ),
    retrieve=extend_schema(
        summary="retrieve crew"
    ),
    update=extend_schema(
        summary="update crew"
    ),
    partial_update=extend_schema(
        summary="partial update crew",
    ),
    create=extend_schema(
        summary="create new crew",
    ),
    destroy=extend_schema(
        summary="delete crew",
    ),
)
class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


@extend_schema_view(
    list=extend_schema(
        summary="get list of route",
    ),
    retrieve=extend_schema(
        summary="retrieve route"
    ),
    update=extend_schema(
        summary="update route"
    ),
    partial_update=extend_schema(
        summary="partial update route",
    ),
    create=extend_schema(
        summary="create new route",
    ),
    destroy=extend_schema(
        summary="delete route",
    ),
)
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type={"type": "str"},
                description="Filter by source  (ex. ?source=krakow)",
            ),
            OpenApiParameter(
                "destination",
                type={"type": "str"},
                description="Filter by destination id (ex. ?destination=london)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary="get list of airplane type",
    ),
    retrieve=extend_schema(
        summary="retrieve airplane type"
    ),
    update=extend_schema(
        summary="update airplane type"
    ),
    partial_update=extend_schema(
        summary="partial update airplane type",
    ),
    create=extend_schema(
        summary="create new airplane type",
    ),
    destroy=extend_schema(
        summary="delete airplane type",
    ),
)
class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


@extend_schema_view(
    list=extend_schema(
        summary="get list of airplane",
    ),
    retrieve=extend_schema(
        summary="retrieve airplane"
    ),
    update=extend_schema(
        summary="update airplane"
    ),
    partial_update=extend_schema(
        summary="partial update airplane",
    ),
    create=extend_schema(
        summary="create new airplane",
    ),
    destroy=extend_schema(
        summary="delete airplane",
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="get list of flight",
    ),
    retrieve=extend_schema(
        summary="retrieve flight"
    ),
    update=extend_schema(
        summary="update flight"
    ),
    partial_update=extend_schema(
        summary="partial update flight",
    ),
    create=extend_schema(
        summary="create new flight",
    ),
    destroy=extend_schema(
        summary="delete flight",
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="get list of order",
    ),
    retrieve=extend_schema(
        summary="retrieve order"
    ),
    update=extend_schema(
        summary="update order"
    ),
    partial_update=extend_schema(
        summary="partial update order",
    ),
    create=extend_schema(
        summary="create new order",
    ),
    destroy=extend_schema(
        summary="delete order",
    ),
)
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
