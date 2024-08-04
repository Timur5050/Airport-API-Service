from rest_framework import serializers

from flights.models import (
    Airport,
    Crew,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Order,
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source="source.name")
    destination_name = serializers.CharField(source="destination.name")

    class Meta:
        model = Route
        fields = ("id", "source_name", "destination_name", "distance")
