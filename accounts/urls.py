from django.urls import path
from .api_views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

name = "accounts"

urlpatterns = [
    path('csrf/', get_csrf_token.as_view(), name='csrf'),
    path('', get_routes, name='routes'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', user_create, name='user_create'),
    path('user/validation/', code_validation, name='code_validation'),
]
