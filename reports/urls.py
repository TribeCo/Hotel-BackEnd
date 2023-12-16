from django.urls import path
from .api_views import *

name = "reports"

urlpatterns = [
    path('reports/food/', FoodSalesReportAPIView.as_view(), name='food-sales-report'),
]
