
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import Food
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
class FoodCreateAPIView(APIView):
    """
        create a food
        {
            "price": 2000,
            "name": "Pizza",
            "meal": "n", --> night
            "type": "text",
            "count": 200
        }
    """
    def post(self, request):
        serializer = FoodSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'food created.','data' : serializer.data}, status=status.HTTP_201_CREATED)

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
            "food_id": 2
        }
    """
    def post(self, request):
        serializer = FoodReservationSerializer(data=request.data)

        if serializer.is_valid():
            food_id = int(serializer.validated_data["food_id"])
            food = Food.objects.get(id=food_id)

            if(food.remain() > 0):
                
                new_reservation = FoodReservation(
                    food=food,
                    user=request.user,
                )
                new_reservation.save()
                food.reserved = food.reserved + 1
                food.save()
                
                return Response({'message': 'food has reserved.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'food is over.'}, status=status.HTTP_400_BAD_REQUEST)
            

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class ReservationAllListAPIView(ListAPIView):
    """List of all Reserves"""
    queryset =  FoodReservation.objects.all()
    serializer_class =  FoodReservationListSerializer
#-----------------------------------------------------------
class UserFoodPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """get food payment for user"""
    def get(self, request):
        payments_objects = request.user.food_reservations.all()
        payments = FoodReservationListSerializer(payments_objects,many = True)

        return Response({'payments': payments.data}, status=status.HTTP_200_OK)
#-----------------------------------------------------------
class FoodImageUpdateView(APIView):
    """Updating food photos"""
    def put(self, request,pk):
        try:
            user = Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({'message':'food not found.'},status=status.HTTP_404_NOT_FOUND) 
        serializer = FoodImageSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'image updated.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class DeliveryChangeView(APIView):
    """Change of delivery mode"""
    def put(self, request,pk):
        try:
            food_rerv = FoodReservation.objects.get(pk=pk)
        except Food.FoodReservation:
            return Response({'message':'food not found.'},status=status.HTTP_404_NOT_FOUND) 
        serializer = DeliveryListSerializer(data=request.data)
        if serializer.is_valid():
            food_rerv.delivery = serializer.validated_data['delivery']
            food_rerv.save()
            return Response({'message':'food reservation updated.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------