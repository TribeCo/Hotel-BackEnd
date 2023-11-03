from django.urls import path
from .api_views import *

name = "accounts"

urlpatterns = [
    path('csrf/', get_csrf_token.as_view(), name='csrf'),
]
