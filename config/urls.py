from django.contrib import admin
from django.urls import path,include
from .settings import admin_url

urlpatterns = [
    path(f'{admin_url}/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
