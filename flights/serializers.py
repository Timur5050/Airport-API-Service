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
