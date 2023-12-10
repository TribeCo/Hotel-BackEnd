from rest_framework import serializers
from .models import *
from accounts.models import *
# -------------------------------------------------------------------------------------------------------------------------------
class RoomTypeSerializer(serializers.ModelSerializer):
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
class RoomSerializer(serializers.ModelSerializer):
    type = RoomTypeSerializer()
    class Meta:
        model = Room
        fields = ('id','number', 'type','has_Resev')
# -------------------------------------------------------------------------------------------------------------------------------
class RoomCreateSerializer(serializers.ModelSerializer):
    type = serializers.IntegerField()
    class Meta:
        model = Room
        fields = ('id','number', 'type','has_Resev')   
# -------------------------------------------------------------------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstName', 'lastName') 
# -------------------------------------------------------------------------------------------------------------------------------
class ReservationListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    room = RoomSerializer()
    remain_paid = serializers.IntegerField(source='remaining')
    total_price = serializers.IntegerField(source='price')
    class Meta:
        model = RoomReservation
        fields = ('room','user','night_count','created','updated','check_in','check_out','paid','been_paid','remain_paid','total_price')
# -------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
