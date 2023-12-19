from django.urls import path
from .api_views import *
from .payments import *

name = "reports"

urlpatterns = [
    path('reports/food/', FoodSalesReportAPIView.as_view(), name='food-sales-report'),
    path('reports/room/', RoomReservationReportAPIView.as_view(), name='room-reservation-report'),
    path('reports/all/', AllReportAPIView.as_view(), name='all-report'),

    path('payment/', PayMoneyAPIView.as_view(), name='pay'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
]
