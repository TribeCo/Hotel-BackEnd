from rest_framework import serializers
from .models import Room,RoomType,RoomReservation
from accounts.models import User
from accounts.serializers import CommentSerializer
#-----------------------------------------------------------
class RoomTypeSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True,required=False)
    class Meta:
        model = RoomType
        fields = ('id', 'type', 'bed_count', 'features', 'price_one_night', 'code','image','comments')
#-----------------------------------------------------------
class ReservationSerializer(serializers.ModelSerializer):
    check_in = serializers.CharField()
    check_out = serializers.CharField()
    room_type_id = serializers.IntegerField()
    nights = serializers.IntegerField()
    class Meta:
        model = RoomType
        fields = ('room_type_id','nights','check_in','check_out')
#-----------------------------------------------------------
class RoomSerializer(serializers.ModelSerializer):
    type = RoomTypeSerializer()
    class Meta:
        model = Room
        fields = ('id','number', 'type','has_Resev')
#-----------------------------------------------------------
class RoomCreateSerializer(serializers.ModelSerializer):
    type = serializers.IntegerField()
    class Meta:
        model = Room
        fields = ('id','number', 'type','has_Resev')   
#-----------------------------------------------------------
class UserSerializerForRoom(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nationalCode', 'firstName', 'lastName', 'role','image']
#-----------------------------------------------------------
class ReservationListSerializer(serializers.ModelSerializer):
    user = UserSerializerForRoom()
    room = RoomSerializer()
    remain_paid = serializers.IntegerField(source='remaining')
    total_price = serializers.IntegerField(source='price')
    date = serializers.CharField(source='shamsi_date')
    class Meta:
        model = RoomReservation
        fields = ('room','user','night_count','created','updated','check_in','check_out','paid','been_paid','remain_paid','total_price','date')
#-----------------------------------------------------------
class RoomTypeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('image',)
        partial = True
#-----------------------------------------------------------
