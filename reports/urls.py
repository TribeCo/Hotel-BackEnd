from django.urls import path
from .api_views import *
from .payments import *

name = "reports"

urlpatterns = [
    path('reports/food/', FoodSalesReportAPIView.as_view(), name='food-sales-report'),
    path('reports/room/', RoomReservationReportAPIView.as_view(), name='room-reservation-report'),
    path('reports/all/', AllReportAPIView.as_view(), name='all-report'),
    path('charts/year/', YearChartAPIView.as_view(), name='charts-year'),
    path('charts/month/', MonthChartAPIView.as_view(), name='charts-month'),
    path('charts/day/', DayChartAPIView.as_view(), name='charts-day'),
    path('charts/food/', FoodSalesChartAPIView.as_view(), name='charts-food'),
    

    path('payment/', PayMoneyAPIView.as_view(), name='pay'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
]
