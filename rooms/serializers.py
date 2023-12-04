from rest_framework import serializers
from .models import *
# -------------------------------------------------------------------------------------------------------------------------------
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('id', 'type', 'bed_count', 'features', 'price_one_night', 'code')
# -------------------------------------------------------------------------------------------------------------------------------
class ReservationSerializer(serializers.ModelSerializer):
    check_in = serializers.CharField()
    check_out = serializers.CharField()
    room_type_id = serializers.IntegerField()
    nights = serializers.IntegerField()
    class Meta:
        model = RoomType
        fields = ('room_type_id','nights','check_in','check_out')
# -------------------------------------------------------------------------------------------------------------------------------
