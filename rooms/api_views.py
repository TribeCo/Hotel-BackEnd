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
class RoomCreateAPIView(APIView):
    """
        {
            "type": "o",
            "bed_count": 2,
            "features": "description about features.",
            "price_one_night": 2000
        }
    """
    def post(self, request):
        serializer = RoomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'room created.','data' : serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
class RoomAllListAPIView(ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomSerializer
# -------------------------------------------------------------------------------------------------------------------------------
class RoomDetailView(RetrieveAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class RoomDeleteView(DestroyAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class RoomUpdateView(UpdateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
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
            print(room_available)

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