
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import Food
from django.utils import timezone
from datetime import date
#-----------------------------------------------------------
"""
    Food reservation and food CRUD are coded in this app.
    api's in api_views.py :

    1- FoodCreateAPIView --> create a food
    2- FoodAllListAPIView --> List of all foods
    3- FoodDetailView  --> Getting the information of a food with ID
    4- FoodDeleteView --> Remove a food with an ID
    5- FoodUpdateView --> Update food information with ID

    6- ReservationRoomAPIView --> Reserve a food
    7- ReservationAllListAPIView  --> List of all Reserves
    8- UserFoodPaymentAPIView --> Report the amount of the user's food reservations
    8- FoodImageUpdateView --> Updating food photos
    9- DeliveryChangeView --> Change of delivery mode

"""
#-----------------------------------------------------------
messages_for_front = {
    'food_created' : 'غذا اضافه شد.',
    'food_reserved' : 'غذا رزرو شد.',
    'food_is_over' : 'موجودی غذا تمام شده است.',
    'food_not_found' : 'غذا پیدا نشد.',
    'image_updated' : 'عکس اپدیت شد.',
    'food_reservation_updated' : 'رزرو غذا اپدیت شد.',
}
#-----------------------------------------------------------
class FoodCreateAPIView(APIView):
    """
        create a food
        {
            "price": 2000,
            "name": "Pizza",
            "description": "text",
            "count": 200
        }
    """
    def post(self, request):
        serializer = FoodSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['food_created'],'data' : serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class FoodAllListAPIView(ListAPIView):
    """List of all foods"""
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
#-----------------------------------------------------------
class FoodDetailView(RetrieveAPIView):
    """Getting the information of a food with ID(domain.com/..../pk/)"""
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'pk'
#-----------------------------------------------------------
class FoodDeleteView(DestroyAPIView):
    """Remove a food with an ID(domain.com/..../pk/)"""
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'pk'
#-----------------------------------------------------------
class FoodUpdateView(UpdateAPIView):
    """Update food information with ID(domain.com/..../pk/)"""
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'pk'
#-----------------------------------------------------------
class ReservationRoomAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
        Reserve a food
        {
            "food_id": 2,
            "meal" : "n"
        }
    """
    def post(self, request):
        serializer = FoodReservationSerializer(data=request.data)

        if serializer.is_valid():
            food_id = int(serializer.validated_data["food_id"])

            try:
                food = Food.objects.get(pk=food_id)
            except Food.DoesNotExist:
                return Response({'message': messages_for_front['food_not_found']},status=status.HTTP_404_NOT_FOUND) 

            if(food.remain() > 0):
                
                new_reservation = FoodReservation(
                    food=food,
                    user=request.user,
                    meal=serializer.validated_data["meal"]
                )
                new_reservation.save()
                food.reserved = food.reserved + 1
                food.save()
                
                return Response({'message': messages_for_front['food_reserved']}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': messages_for_front['food_is_over']}, status=status.HTTP_400_BAD_REQUEST)
            

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class ReservationAllListAPIView(ListAPIView):
    """List of all Reserves"""
    serializer_class =  FoodReservationListSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return FoodReservation.objects.filter(created=today)
#-----------------------------------------------------------
class UserFoodPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """get food payment for user"""
    def get(self, request):
        payments_objects = request.user.food_reservations.all().filter(paid=False)
        payments = FoodReservationListSerializer(payments_objects,many = True)

        return Response({'payments': payments.data}, status=status.HTTP_200_OK)
#-----------------------------------------------------------
from datetime import date, datetime
class TodayUserPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """get food payment for user"""
    def get(self, request):
        today = date.today()
        food_reservations = FoodReservation.objects.filter(user=request.user, created=today)
        payments = FoodReservationListSerializer(food_reservations,many = True)

        return Response({'payments': payments.data}, status=status.HTTP_200_OK)
#-----------------------------------------------------------
class FoodImageUpdateView(APIView):
    """Updating food photos"""
    def put(self, request,pk):
        try:
            food = Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({'message': messages_for_front['food_not_found']},status=status.HTTP_404_NOT_FOUND) 
        serializer = FoodImageSerializer(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':messages_for_front['image_updated'],'data' : f"https://hotelt.liara.run/images/{food.image}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class DeliveryChangeView(APIView):
    """Change of delivery mode"""
    def put(self, request,pk):
        try:
            food_rerv = FoodReservation.objects.get(pk=pk)
        except Food.FoodReservation:
            return Response({'message': messages_for_front['food_not_found']},status=status.HTTP_404_NOT_FOUND) 
        serializer = DeliveryListSerializer(data=request.data)
        if serializer.is_valid():
            food_rerv.delivery = serializer.validated_data['delivery']
            food_rerv.save()
            return Response({'message': messages_for_front['food_reservation_updated']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------