from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from .serializers import RoomTypeSerializer,RoomSerializer,ReservationListSerializer,RoomCreateSerializer,RoomTypeImageSerializer,ReservationSerializer
from .models import RoomType,Room,RoomReservation
#--------------------------------------------------------
"""
    Food reservation and food CRUD are coded in this app.
    api's in api_views.py :

    1- RoomTypeAllListAPIView --> get a list of all types of hotel rooms.
    2- RoomTypeDetailView --> Get information of a specific type of room.
    3- RoomTypeCreateAPIView  --> api to create an object from the room type.
    4- RoomTypeDeleteView --> delete an object from the room type with pk.
    5- RoomTypeUpdateView --> update information an object from the room type with pk.
    6- RoomTypeImageUpdateView --> update image of an object from the room type with pk.

    7- RoomAllListAPIView  --> get list of all room in hotel.
    8- RoomDetailView --> Get information of a specific type of room.
    9- RoomCreateAPIView --> api to create an object from the room.
    10- RoomDeleteView --> delete an object from the room with pk
    11- RoomUpdateView  --> update information an object from the room with pk.
    
    12- ReservationRoomAPIView --> Book a room for a few nights
    13- ReservationAllListAPIView --> Get list of all reservations in hotel.
    14- UserPaymentAPIView --> Get the list of all the user's reservations in the hotel.

"""
#--------------------------------------------------------
class RoomTypeAllListAPIView(ListAPIView):
    """get a list of all types of hotel rooms.(domain.com/..../rooms/type/)"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
#--------------------------------------------------------
class RoomTypeDetailView(RetrieveAPIView):
    """Get information of a specific type of room.(domain.com/..../rooms/type/<int:pk>/)"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    lookup_field = 'pk'
#--------------------------------------------------------
class RoomTypeCreateAPIView(APIView):
    """
        api to create an object from the room type.(domain.com/..../rooms/type/create/)"
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

#--------------------------------------------------------
class RoomTypeDeleteView(DestroyAPIView):
    """delete an object from the room type with pk.(domain.com/..../rooms/type/delete/<int:pk>/)"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    lookup_field = 'pk'
#--------------------------------------------------------
class RoomTypeUpdateView(UpdateAPIView):
    """update information an object from the room type with pk.(domain.com/..../rooms/type/update/<int:pk>/)"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    lookup_field = 'pk'
#--------------------------------------------------------
class RoomTypeImageUpdateView(APIView):
    """update image of an object from the room type with pk.(domain.com/..../rooms/type/update/image/<int:pk>/)"""
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
#--------------------------------------------------------
class RoomAllListAPIView(ListAPIView):
    """get list of all room in hotel.(domain.com/..../rooms/)"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
#--------------------------------------------------------
class RoomDetailView(RetrieveAPIView):
    """Get information of a specific type of room.(domain.com/..../rooms/<int:pk>/)"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
#--------------------------------------------------------
class RoomCreateAPIView(APIView):
    """
        api to create an object from the room.(domain.com/..../rooms/create/)"
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
#--------------------------------------------------------
class RoomDeleteView(DestroyAPIView):
    """delete an object from the room with pk.(domain.com/..../rooms/delete/<int:pk>/)"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
#--------------------------------------------------------
class RoomUpdateView(UpdateAPIView):
    """update information an object from the room with pk.(domain.com/..../rooms/update/<int:pk>/)"""
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
#--------------------------------------------------------
class ReservationRoomAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
        Book a room for a few nights(domain.com/..../rooms/reservation/)
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
                return Response({'message': 'Room reserved successfully.'}, status=status.HTTP_400_BAD_REQUEST)

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
            
            return Response({'message': 'Room reserved successfully.'}, status=status.HTTP_201_CREATED)
            

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------
class ReservationAllListAPIView(ListAPIView):
    """Get list of all reservations in hotel.(domain.com/..../rooms/reservation/all/)"""
    queryset =  RoomReservation.objects.all()
    serializer_class =  ReservationListSerializer
#--------------------------------------------------------
class UserPaymentAPIView(APIView):
    """Get the list of all the user's reservations in the hotel.(domain.com/..../rooms/reservation/user/)"""
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationListSerializer
    """
        get payment for user
    """
    def get(self, request):
        payments_objects = request.user.reservations.all()
        payments = ReservationListSerializer(payments_objects,many = True)

        return Response({'payments': payments.data}, status=status.HTTP_200_OK)
#--------------------------------------------------------
