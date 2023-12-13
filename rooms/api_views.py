from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from rest_framework import permissions
from rest_framework.views import APIView
from .models import *
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
# -------------------------------------------------------------------------------------------------------------------------------
class RoomTypeAllListAPIView(ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
# -------------------------------------------------------------------------------------------------------------------------------
class RoomTypeDetailView(RetrieveAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class RoomTypeCreateAPIView(APIView):
    """
        {
            "type": "o",
            "bed_count": 2,
            "features": "description about features.",
            "price_one_night": 2000
        }
    """
    def post(self, request):
        serializer = RoomTypeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'room created.','data' : serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------------------------------------------------------------------------------------------------------
class RoomTypeDeleteView(DestroyAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class RoomTypeUpdateView(UpdateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class RoomAllListAPIView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
# -------------------------------------------------------------------------------------------------------------------------------
class RoomDetailView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class RoomCreateAPIView(APIView):
    """
        {
            "type": 1,
            "number": 2
        }
    """
    def post(self, request):
        serializer = RoomCreateSerializer(data=request.data)

        if serializer.is_valid():

            try:
                room_type = RoomType.objects.get(id=serializer.validated_data['type'])
            except RoomType.DoesNotExist:
                 return Response({'message': 'room type does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            
            room = Room(number = serializer.validated_data['number'],
                type = room_type
            )
            room.save()

            return Response({'message': 'room created.','data' : f"room id: {room.id}"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
class RoomDeleteView(DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class RoomUpdateView(UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        room_id = self.kwargs['pk']
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                room_type = RoomType.objects.get(id=serializer.validated_data['type'])
            except RoomType.DoesNotExist:
                return Response({'message': 'room type does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                room = Room.objects.get(id=room_id)
            except Room.DoesNotExist:
                return Response({'message': 'room does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            room.number = serializer.validated_data['number']
            room.type = room_type
            room.save()

            return Response({'message': 'room updated.', 'data': f"room id: {room.id}"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
class ReservationRoomAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
        {
            "room_type_id": 2,
            "nights": 4,
            "check_in": "2023-12-01 14:00:00",
            "check_out": "2023-12-03 12:00:00"
        }
    """
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():
            room_type_id = int(serializer.validated_data["room_type_id"])
            check_in = datetime.strptime(serializer.validated_data["check_in"], "%Y-%m-%d %H:%M:%S")
            check_out = datetime.strptime(serializer.validated_data["check_out"], "%Y-%m-%d %H:%M:%S")
            room_type = RoomType.objects.get(id=room_type_id)
            room_available = room_type.rooms.filter(has_Resev=False)

            if(room_available.count() == 0):
                return Response({'message': 'not found free room.'}, status=status.HTTP_400_BAD_REQUEST)

            reservation_room = room_available[0]

            new_reservation = RoomReservation(
                room=reservation_room,
                user=request.user,
                night_count=serializer.validated_data["nights"],
                check_in=check_in,
                check_out=check_out
            )
            new_reservation.save()
            reservation_room.has_Resev = True
            reservation_room.save()
            
            return Response({'message': 'room has reserved.'}, status=status.HTTP_201_CREATED)
            

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
class ReservationAllListAPIView(ListAPIView):
    queryset =  RoomReservation.objects.all()
    serializer_class =  ReservationListSerializer
# -------------------------------------------------------------------------------------------------------------------------------
class UserPaymentAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReservationListSerializer
    """
        get payment for user
    """
    def get(self, request):
        payments_objects = request.user.reservations.all()
        payments = ReservationListSerializer(payments_objects,many = True)

        return Response({'payments': payments.data}, status=status.HTTP_200_OK)
# -------------------------------------------------------------------------------------------------------------------------------
class RoomTypeImageUpdateView(APIView):
    def put(self, request,pk):
        try:
            user = RoomType.objects.get(pk=pk)
        except RoomType.DoesNotExist:
            return Response({'message':'RoomType not found.'},status=status.HTTP_404_NOT_FOUND) 
        serializer = RoomTypeImageSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'image updated.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
