
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from rest_framework import permissions
from rest_framework.views import APIView
from .models import Room
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
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
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
# -------------------------------------------------------------------------------------------------------------------------------
class RoomDetailView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class RoomDeleteView(DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class RoomUpdateView(UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------