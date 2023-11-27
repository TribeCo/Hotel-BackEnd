from rest_framework import serializers
from .models import *
# -------------------------------------------------------------------------------------------------------------------------------
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('id', 'type', 'bed_count', 'features', 'price_one_night', 'code')
# -------------------------------------------------------------------------------------------------------------------------------
