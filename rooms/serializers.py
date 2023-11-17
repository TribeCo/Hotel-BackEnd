from rest_framework import serializers
from .models import *
# -------------------------------------------------------------------------------------------------------------------------------
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'type', 'bed_count', 'features', 'price_one_night', 'has_Resev', 'code')
# -------------------------------------------------------------------------------------------------------------------------------
