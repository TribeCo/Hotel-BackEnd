from django.urls import path
from .api_views import *

name = "Food"

urlpatterns = [
    path('food/create/', FoodCreateAPIView.as_view(), name='food-create'),
    path('food/', FoodAllListAPIView.as_view(), name='all-food-list'), 
    path('food/<int:pk>/', FoodDetailView.as_view(), name='food-detail'),
    path('food/delete/<int:pk>/', FoodDeleteView.as_view(), name='food-delete'),
    path('food/update/<int:pk>/', FoodUpdateView.as_view(), name='food-update')
]
