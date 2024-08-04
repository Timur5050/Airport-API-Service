from users.views import CreateUser, RetrieveUpdateUser

from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("register/", CreateUser.as_view(), name="register"),
    path("me/", RetrieveUpdateUser.as_view(), name="manage"),
]

app_name = "users"
