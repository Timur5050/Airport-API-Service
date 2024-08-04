from users.serializers import UserSerializer

from django.contrib.auth import get_user_model
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin
)
from rest_framework.generics import CreateAPIView


class CreateUser(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

