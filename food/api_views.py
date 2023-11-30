
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from .serializers import *
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