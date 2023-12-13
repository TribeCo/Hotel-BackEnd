from django.urls import path
from .api_views import *

name = "Food"

urlpatterns = [
    path('food/', FoodAllListAPIView.as_view(), name='all-food-list'), 
    path('food/<int:pk>/', FoodDetailView.as_view(), name='food-detail'),
    path('food/create/', FoodCreateAPIView.as_view(), name='food-create'),
    path('food/delete/<int:pk>/', FoodDeleteView.as_view(), name='food-delete'),
    path('food/update/<int:pk>/', FoodUpdateView.as_view(), name='food-update'),
    path('food/update/image/<int:pk>/', FoodImageUpdateView.as_view(), name='food-update-image'),
    path('food/reservation/', ReservationRoomAPIView.as_view(), name='food-reservation'),
    path('food/reservation/all/', ReservationAllListAPIView.as_view(), name='food-list-reservation'),
    path('food/reservation/user/', UserFoodPaymentAPIView.as_view(), name='user-food-reservation'),

]
