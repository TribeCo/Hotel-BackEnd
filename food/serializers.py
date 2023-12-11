from rest_framework import serializers
from .models import *
# -------------------------------------------------------------------------------------------------------------------------------
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('price', 'name', 'meal', 'type', 'count','day','id')
# -------------------------------------------------------------------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstName', 'lastName') 
# -------------------------------------------------------------------------------------------------------------------------------
class FoodReservationListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    food = FoodSerializer()
    remain_paid = serializers.IntegerField(source='remaining')
    total_price = serializers.IntegerField(source='price')
    class Meta:
        model = FoodReservation
        fields = ('food','user','created','paid','been_paid','remain_paid','total_price')
# -------------------------------------------------------------------------------------------------------------------------------
class FoodReservationSerializer(serializers.ModelSerializer):
    food_id = serializers.IntegerField()
    class Meta:
        model = Food
        fields = ('food_id',)
# -------------------------------------------------------------------------------------------------------------------------------
class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('image',)
        partial = True
# -------------------------------------------------------------------------------------------------------------------------------