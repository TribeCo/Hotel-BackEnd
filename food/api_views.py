
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import Food
# -------------------------------------------------------------------------------------------------------------------------------
class FoodCreateAPIView(APIView):
    """
        {
            "price": 2000,
            "name": "Joje",
            "meal": "m",
            "type": "text",
            "count": 200
        }
    """
    def post(self, request):
        serializer = FoodSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'room created.','data' : serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
class FoodAllListAPIView(ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
# -------------------------------------------------------------------------------------------------------------------------------
class FoodDetailView(RetrieveAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class FoodDeleteView(DestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class FoodUpdateView(UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class ReservationRoomAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
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
# -------------------------------------------------------------------------------------------------------------------------------
class ReservationAllListAPIView(ListAPIView):
    queryset =  FoodReservation.objects.all()
    serializer_class =  FoodReservationListSerializer
# -------------------------------------------------------------------------------------------------------------------------------
class UserFoodPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
        get food payment for user
    """
    def get(self, request):
        payments_objects = request.user.food_reservations.all()
        payments = FoodReservationListSerializer(payments_objects,many = True)

        return Response({'payments': payments.data}, status=status.HTTP_200_OK)
# -------------------------------------------------------------------------------------------------------------------------------
class FoodImageUpdateView(APIView):
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
# -------------------------------------------------------------------------------------------------------------------------------