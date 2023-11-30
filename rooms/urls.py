from django.urls import path
from .api_views import *

name = "rooms"

urlpatterns = [
    path('rooms/create/', RoomCreateAPIView.as_view(), name='room-create'),
    path('rooms/', RoomAllListAPIView.as_view(), name='all-room-list'), 
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/delete/<int:pk>/', RoomDeleteView.as_view(), name='room-delete'),
    path('rooms/update/<int:pk>/', RoomUpdateView.as_view(), name='room-update')
]
